// Fetch a release of the Cruor framework and check it.
//
//   node examples/fetch-release.mjs <address> <folder> [--manifest-sha256 <sha256>]
//
// <address> is where the release's files are served, for example
//   https://github.com/crussella0129/cruor-framework/releases/download/v0.1.0/
// <folder> is where to put them; it is made if it is not there.
//
// It fetches manifest.json, then every file the manifest lists, and keeps a
// file only if its size and SHA-256 are the ones the manifest gives. Give
// --manifest-sha256 the SHA-256 of the manifest you expect, kept beside the
// version in your own build, and you get exactly the files you expect.
// Without it, the check shows only that the files and the manifest agree
// with each other.
//
// It exits 0 if every file was fetched and checked, and otherwise says what
// went wrong and exits 1. It needs Node 20 or newer and nothing else. It is
// an example: copy it into a build and change it to suit.

import { createHash } from 'node:crypto';
import { mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const MANIFEST = 'manifest.json';

class Failure extends Error {}

const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');

function readArguments(argv) {
  const plain = [];
  let manifestSha256 = null;
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === '--manifest-sha256') {
      manifestSha256 = argv[index + 1];
      index += 1;
    } else {
      plain.push(argv[index]);
    }
  }
  const usage =
    'usage: node examples/fetch-release.mjs <address> <folder> [--manifest-sha256 <sha256>]';
  if (plain.length !== 2) throw new Failure(usage);
  if (manifestSha256 !== null && !/^[0-9a-f]{64}$/.test(manifestSha256 ?? '')) {
    throw new Failure(`--manifest-sha256 takes sixty-four hexadecimal characters\n${usage}`);
  }
  const [address, folder] = plain;
  return { address: address.endsWith('/') ? address : `${address}/`, folder, manifestSha256 };
}

async function fetchBytes(address, name) {
  const url = new URL(name, address);
  let response;
  try {
    response = await fetch(url);
  } catch (error) {
    const reason = error.cause?.code ?? error.cause?.message ?? error.message;
    throw new Failure(`cannot reach ${url}: ${reason}`);
  }
  if (!response.ok) throw new Failure(`cannot fetch ${url}: HTTP ${response.status}`);
  return Buffer.from(await response.arrayBuffer());
}

// A name a release may give a file: one bare file name, nothing that could
// lead out of the folder it is written to.
const isBareName = (name) =>
  typeof name === 'string' && /^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(name) && !name.includes('..');

async function main() {
  const { address, folder, manifestSha256 } = readArguments(process.argv.slice(2));

  const manifestBytes = await fetchBytes(address, MANIFEST);
  if (manifestSha256 !== null && sha256(manifestBytes) !== manifestSha256) {
    throw new Failure(
      `${MANIFEST} is not the one expected: its SHA-256 is ${sha256(manifestBytes)}, not ${manifestSha256}`,
    );
  }

  let manifest;
  try {
    manifest = JSON.parse(manifestBytes.toString('utf8'));
  } catch (error) {
    throw new Failure(`${MANIFEST} cannot be read: ${error.message}`);
  }
  if (!Array.isArray(manifest.files) || manifest.files.length === 0) {
    throw new Failure(`${MANIFEST} lists no files`);
  }
  // Every name is judged before any file is fetched.
  for (const file of manifest.files) {
    if (!isBareName(file?.name) || file.name === MANIFEST) {
      throw new Failure(
        `${MANIFEST} lists ${JSON.stringify(file?.name)}, which is not a bare file name`,
      );
    }
  }

  await mkdir(folder, { recursive: true });
  for (const file of manifest.files) {
    const bytes = await fetchBytes(address, file.name);
    if (bytes.length !== file.size || sha256(bytes) !== file.sha256) {
      throw new Failure(
        `${file.name} is not the file the manifest lists: it is ${bytes.length} bytes with SHA-256 ` +
          `${sha256(bytes)}; the manifest has ${file.size} bytes and ${file.sha256}`,
      );
    }
    // Written only once it has been checked.
    await writeFile(join(folder, file.name), bytes);
  }
  await writeFile(join(folder, MANIFEST), manifestBytes);

  console.log(
    `fetch-release: ${manifest.files.length} files of ${manifest.framework ?? 'the release'} ` +
      `${manifest.version ?? ''} fetched into ${folder} and checked`,
  );
}

main().catch((error) => {
  if (!(error instanceof Failure)) throw error;
  console.error(`fetch-release: ${error.message}`);
  process.exitCode = 1;
});

# INT-0005 — Versioned releases that a build fetches

<!-- sprint-loop-intent-v2 -->
- **Intent ID:** INT-0005
- **State:** proposed
- **Work evidence:** none
- **Completion evidence:** none
- **Code evidence:** none
- **Test evidence:** none
- **Documentation evidence:** none

## Intent

A page takes the framework in by fetching the files of a numbered release
when it builds. The owner chose this on 23 November 2026 ("Versioned
release, fetched").

Each version of the framework is a tagged release on GitHub. A release
holds the framework's files (the fonts and their stylesheet and licence;
later the tokens, the look's stylesheet and the theme file), each to be had
on its own and all together as one archive, with a manifest of SHA-256
checksums. A build names the version it wants, fetches the files, and can
check each against the manifest. A page that builds this way keeps no font
file in its own repository.

Boundaries:

- No npm package for now.
- The framework does not serve the files to readers' browsers. A page
  fetches them when it builds and serves them from its own origin.
- Publishing a release is done on the owner's word, each time.

## Acceptance criteria

1. One command puts a release together from the repository's tracked files:
   the files themselves, one archive of them, and a manifest giving each
   file's name, size and SHA-256.
2. The same commit always gives the same manifest.
3. The stylesheets in a release refer to the fonts by relative address, so
   they work unchanged wherever the files are served together.
4. A build that fetches a release's files over HTTP and checks each against
   the manifest ends with files identical to the repository's.
5. Pushing a version tag publishes that version's release with those files.
6. The README gives the address pattern of a release's files and shows how
   a build fetches and checks them.

## Rationale

It is how Tome takes in its font today: a script fetches the file when Tome
builds, and no font file is tracked there. A release on GitHub needs no
other account or service, suits a page built in any language, and a pinned
version with checksums means a build gets exactly what it expects.

## Alternatives

- **An npm package.** Convenient for Node projects, but it means another
  account and a published name, and suits a page built in Rust or written
  by hand less.
- **Both from the start.** Two channels to keep in step before there is a
  second user.
- **Pages link the files straight from the repository.** Not promised: a
  release is the thing a page should name.

## Consequences

- Version numbers mean something from the first release: a change to a
  font file or a token is a new version.
- An npm package can be added later as its own intent without changing
  what a release is.

## Transition history
- 2026-11-23: created as `proposed` in Sprint 0's Research, from the owner's
  answer that day.

# INT-0005 — Versioned releases that a build fetches

<!-- sprint-loop-intent-v2 -->
- **Intent ID:** INT-0005
- **State:** active
- **Work evidence:** [T-008 to T-012, Sprint 0 build plan](../sprints/s0/sprint-plans/build-plan.md), [T-102 backlog](../work/tasks.md)
- **Completion evidence:** [T-008 to T-012, completed tasks](../work/completed-tasks.md)
- **Code evidence:** [src/bundle.rs](../../src/bundle.rs), [examples/fetch-release.mjs](../../examples/fetch-release.mjs), [.github/workflows/release.yml](../../.github/workflows/release.yml), [tools/release-gate.sh](../../tools/release-gate.sh)
- **Test evidence:** [Sprint 0 test report](../sprints/s0/sprint-tests/test-report.md)
- **Documentation evidence:** [README](../../README.md)

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
file in its own repository. The first release, 0.1.0, holds the fonts
alone.

Boundaries:

- No npm package for now.
- The framework does not serve the files to readers' browsers. A page
  fetches them when it builds and serves them from its own origin.
- Publishing a release is done on the owner's word, each time. A version
  tag is pushed only then, and only a tagged commit on `main` is published.

## Acceptance criteria

1. One command puts a release together from the repository's tracked files:
   the files themselves, one archive of them, and a manifest giving each
   file's name, size and SHA-256. The archive holds the manifest, so the
   manifest cannot list it; the archive has a checksum file of its own.
2. The same commit always gives the same manifest.
3. The stylesheets in a release refer to the fonts by relative address, so
   they work unchanged wherever the files are served together.
4. A build that fetches a release's files over HTTP and checks each against
   the manifest ends with files identical to the repository's.
5. Pushing a version tag on `main` publishes that version's release with
   those files, whole or not at all and never over a release that exists,
   and the release then proves itself: its files are fetched from its own
   address and checked.
6. The README gives the address pattern of a release's files and shows how
   a build fetches and checks them.

## Rationale

It is how Tome takes in its font today: a script fetches the file when Tome
builds, and no font file is tracked there. A release on GitHub needs no
other account or service, suits a page built in any language, and a pinned
version with checksums means a build gets exactly what it expects. The
checksum a build pins is the manifest's own: with that one value fixed
beside the version, every file the manifest lists is fixed too. Without it,
checking shows only that the files and the manifest agree with each other.

## Alternatives

- **An npm package.** Convenient for Node projects, but it means another
  account and a published name, and suits a page built in Rust or written
  by hand less.
- **Both from the start.** Two channels to keep in step before there is a
  second user.
- **Pages link the files straight from the repository.** Not promised: a
  release is the thing a page should name.
- **A protected environment with the owner as required reviewer**, so that
  GitHub itself holds a release until the owner approves it. Not taken: it
  is a setting of the repository the owner would have to keep, and a tag is
  pushed only on the owner's word. The workflow refuses a tag that is not
  on `main` or already has a release.

## Consequences

- Version numbers mean something from the first release: a change to a
  font file or a token is a new version.
- An npm package can be added later as its own intent without changing
  what a release is.

## Transition history
- 2026-11-23: created as `proposed` in Sprint 0's Research, from the owner's
  answer that day.
- 2026-11-23: `proposed` to `planned`. The owner approved Sprint 0's plan, which builds the release command, the worked example of fetching, the publishing workflow and the README's account of them (T-008 to T-011). No release is published in the sprint; the first tag waits for the owner's word.
- 2026-11-23: revised after the plan's review, still `planned`. Criterion 1
  now accounts for the archive; criterion 5 and the Boundaries say what may
  be published and that a release checks itself; the Intent says the first
  release holds the fonts alone. T-102 records the first release's own
  check.
- 2026-11-23: revised after the plan's second review, still `planned`. The
  Rationale now says that the checksum a build pins is the manifest's, and
  the Alternatives record the protected environment.
- 2026-11-23: `planned` to `active`. Sprint 0's Build reached T-008, the
  command that puts a release together.
- 2026-11-23: Test evidence attached, still `active`. Sprint 0's Test
  phase proved criteria 1 to 4 and 6. Criterion 5 is built and tested
  short of a real release; the release's own check of itself cannot run
  until `v0.1.0` is pushed on the owner's word (backlog task T-102), and
  the intent is not `realized` before that run has passed.

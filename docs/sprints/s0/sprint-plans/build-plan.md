# Sprint 0 Build Plan

## Intents
- [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) — state: planned; acceptance criteria covered: 1, 2, 3, 4, 5 and 6 (all).
- [INT-0005](../../../intents/INT-0005-versioned-releases.md) — state: planned; acceptance criteria covered: 1, 2, 3, 4 and 6. Criterion 5 is built here (T-010) and proven when the first version tag is pushed, which waits for the owner's word after this sprint's pull request is merged; the release then checks itself, and backlog task T-102 records that run.
- [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) — state: planned; acceptance criteria covered: 1, 3 and 5. Criteria 2 and 4 wait for the look ([INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md), [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md)), which this sprint does not build.

The owner approved this plan on 23 November 2026. What that approval
settled is recorded in the intents: which build of Cruor is taken in and
the wording of the copyright line (INT-0002), the languages of the tool and
its checks (INT-0001), and that the first release holds the fonts alone and
is published only on the owner's word (INT-0005).

## Schema Tree
- The framework holds Cruor's fonts and is ready to release them
  - Ground
    - T-001: the tool's crate, the check environment, the guards and CI
    - T-002: the code's licences
  - The fonts
    - T-003: take the fonts in, with their licence and the list of families
    - T-004: `css` writes and checks the stylesheet
    - T-005: `manifest` writes and checks the checksums
    - T-006: a check that each font agrees with its rule
    - T-007: a page that sets a line in every face
  - The release
    - T-008: `bundle` puts a release together
    - T-009: the worked example of a build fetching a release
    - T-010: the workflow that publishes a release on a version tag
    - T-012: CI bundles on every push and keeps the result
  - The front door
    - T-011: the README
  - The rule
    - T-013: the review that keeps the repository in its own terms

Layout the sprint creates:

```text
fonts/       32 .woff2, OFL.txt, families.toml, fonts.css, manifest.toml,
             specimen.html (one flat folder)
src/         the Rust tool
tools/       check_fonts.py, run-guards.sh, requirements.txt
examples/    fetch-release.mjs
tests/       Rust and Python tests
LICENSE-MIT  LICENSE-APACHE  README.md  Cargo.toml  Cargo.lock
rust-toolchain.toml  pyproject.toml  .gitattributes
.github/workflows/ci.yml  .github/workflows/release.yml
```

The fonts, their stylesheet and their licence are kept in one flat folder
because a release on GitHub has no folders. The stylesheet names each font
by its bare file name, so the same files work in the repository, in an
archive and as a release.

The tool is run as `cargo run --release -- <command>`. Its commands are
`css`, `manifest`, `check` (both checks at once) and `bundle`.

**Tests land with their task.** Each task's commit carries the tests the
test plan names for it, under `tests/`, and those paths are part of what
the task touches. The guards are green at every task's commit.

**Order.** Tasks are taken in the order below, which is not the order of
their numbers: T-013 follows T-003. No commit of this sprint's Build is
pushed before T-013's first review is recorded.

## Execution Sequence

### T-001: Set up the tool's crate, the check environment, the guards and CI
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)
- **Touches:** Cargo.toml, Cargo.lock, rust-toolchain.toml, src/main.rs, pyproject.toml, tools/requirements.txt, tools/run-guards.sh, .github/workflows/ci.yml, .gitignore, .gitattributes, tests/
- **Depends on:** (none)
- **Acceptance criterion:** INT-0002 criterion 5, "A check fails if…": the checks need a place to live and something that runs them.
- **Success criterion (EARS):**
  - **WHEN** `cargo run --release -- --help` is run on a clean checkout, **THEN** the tool **SHALL** exit 0 and name the commands `css`, `manifest`, `check` and `bundle`.
  - **WHEN** `bash tools/run-guards.sh` is run, **THEN** it **SHALL** run `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`, `ruff format --check`, `ruff check` and `pytest`, and **SHALL** exit non-zero if any of them fails.
  - **WHEN** a commit is pushed to `main` or `dev`, or a pull request is opened, **THEN** CI **SHALL** run `tools/run-guards.sh` and fail if it fails.
  - **WHEN** the repository is checked out on any system, **THEN** every text file **SHALL** arrive with line feeds for line ends and every `.woff2` unchanged, as `.gitattributes` directs.
  - **WHEN** `Cargo.toml` is read, **THEN** the crate's version **SHALL** be `0.1.0`, the number of the first release.
- **Notes:** this task provisions everything later tasks need, so none of them has to touch these files again: every crate the tool will use (clap, serde, toml, serde_json, sha2, zip), the pinned Rust toolchain, the Python packages at pinned versions (pytest, fontTools with Brotli, Playwright, ruff), and in CI the browser Playwright drives and Node 20. `pyproject.toml` holds the settings of ruff and pytest. The README (T-011) names these as requirements; nothing here records setting up a machine. `.gitignore` gains `target/` and `dist/`. It is scaffolding, accepted as one commit: no part of it can be judged without the rest.

### T-002: Add the code's licences
- **Intent:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)
- **Touches:** LICENSE-MIT, LICENSE-APACHE, Cargo.toml, tests/
- **Depends on:** T-001
- **Acceptance criterion:** INT-0001 criterion 3, "`LICENSE-MIT` and `LICENSE-APACHE` stand at the root".
- **Success criterion (EARS):**
  - **WHEN** the root of the repository is listed, **THEN** it **SHALL** hold `LICENSE-MIT`, with the MIT licence's text and the line "Copyright (c) 2026 Charles Russella", and `LICENSE-APACHE`, with the text of the Apache License, Version 2.0.
  - **WHEN** `Cargo.toml` is read, **THEN** its `license` field **SHALL** be `MIT OR Apache-2.0`.
- **Notes:** the README's part of criterion 3 is T-011.

### T-003: Take the fonts in, with their licence and the list of families
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)
- **Touches:** fonts/*.woff2, fonts/OFL.txt, fonts/families.toml, tests/
- **Depends on:** T-001
- **Acceptance criterion:** INT-0002 criteria 1, 2 and 6.
- **Success criterion (EARS):**
  - **WHEN** `fonts/` is listed, **THEN** it **SHALL** hold exactly thirty-two `.woff2` files, named `<stem>-<style>.woff2` for the stems `CruorSansRegular`, `CruorLiteRegular`, `CruorThornamentalRegular`, `CruorSansMono`, `CruorLiteMono`, `CruorThornamentalMono`, `CruorSansPixelated` and `CruorPixelated` and the styles `Regular`, `Bold`, `Italic` and `BoldItalic`.
  - **WHEN** `fonts/OFL.txt` is read, **THEN** it **SHALL** hold the text of the SIL Open Font License, Version 1.1, beneath the copyright line that INT-0002 criterion 2 gives.
  - **WHEN** `fonts/families.toml` is read, **THEN** it **SHALL** list the eight families, each with its name as the fonts give it, its file stem, and its kind (`proportional`, `mono` or `pixel`).
  - **WHEN** the repository's tracked files are listed, **THEN** the only font files among them (`.woff2`, `.woff`, `.ttf`, `.otf`) **SHALL** be those thirty-two.
- **Notes:** the fonts come from a clean build of the Cruor project at the head of its working branch when this task runs, as INT-0002 records. The build is made in a scratch copy outside both repositories, from a tree with nothing uncommitted, and only the thirty-two `.woff2` files are copied in. The full commit id is noted for T-005, which records it. The fonts go in as that build makes them, whatever their own licence and embedding fields say (INT-0002, Consequences; backlog task T-101). The review of T-013 covers this commit before it is pushed. The commit message says which build of Cruor the fonts are, and nothing about any machine.

### T-013: Keep the repository in its own terms, by review before every push
- **Intent:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)
- **Touches:** docs/sprints/s0/sprint-tests/own-terms-review.md
- **Depends on:** T-003
- **Acceptance criterion:** INT-0001 criterion 5, "Nothing in the repository or its history names another typeface or describes Cruor by comparison with one"; and [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) criterion 6, for files of any kind.
- **Success criterion (EARS):**
  - **WHEN** commits are about to be pushed, **THEN** a review made from outside the repository **SHALL** search, for every commit not yet pushed, the content of every file that commit adds or changes and the commit's message, against a list of the names of other typefaces that is kept outside the repository, and **SHALL** read the new prose of those commits once for any description of Cruor by comparison with another typeface.
  - **WHEN** the commits to be pushed include font files, **THEN** the review **SHALL** also read every name-table string of each font with fontTools and search those, and **SHALL** read each font's WOFF2 metadata block and private block in the same way or record that the font has none.
  - **WHEN** a pull request, a tag or a release is about to be made, **THEN** the same search and reading **SHALL** be made of its title, its body and its message first.
  - **WHEN** a pull request arrives that the owner did not write (the dependency updater's), **THEN** its title, body and commits **SHALL** be searched and read before it is merged, and one in which something is found **SHALL** be closed, not merged.
  - **WHEN** a review is made, **THEN** `own-terms-review.md` **SHALL** gain an entry giving the date, the first and last commit covered, what else was covered, and the number found, which **SHALL** be none before the push goes ahead.
  - **WHEN** the review covers the commit that takes the fonts in, **THEN** its entry **SHALL** give the full commit id of Cruor that was built, state that the build's tree had nothing uncommitted, and set the thirty-two fonts' glyph counts and family names against `font-inventory.md`, recording every difference.
  - **WHEN** a review finds something in a commit not yet pushed, **THEN** that commit **SHALL** be rewritten before any push; and **WHEN** it finds something already public, **THEN** work **SHALL** stop for the owner.
  - **WHEN** a review is made, **THEN** it **SHALL** also list the files each covered commit adds or changes and compare them with what the commit's task touches, and anything outside **SHALL** be accounted for in the entry or removed before the push.
- **Notes:** the review is made from outside because a check inside the repository would have to hold the names it forbids. This task is complete when the review that covers T-003's commit is recorded; the reviews before later pushes add their entries to the same file. A commit whose only change is a new entry in that file is covered by the entry it adds. The Test phase reads the record as it stands then; the reviews before the pushes that close the sprint and open its pull request are added to the same file and read at the Loop phase, before the pull request is opened. The Book's own ledgers and records, which the commit helper changes with each task, are accounted for as such.

### T-004: Write and check the stylesheet from the list of families
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)
- **Touches:** src/ (the reader of `families.toml`, and the `css` command), fonts/fonts.css, tests/
- **Depends on:** T-003
- **Acceptance criterion:** INT-0002 criterion 3, "One stylesheet declares every family under its own name with its four styles joined".
- **Success criterion (EARS):**
  - **WHEN** `css` is run, **THEN** `fonts/fonts.css` **SHALL** hold exactly thirty-two `@font-face` rules, one for each family and style, each with `font-family` set to the family's name, `font-weight` 400 for Regular and Italic and 700 for Bold and Bold Italic, `font-style` `normal` or `italic`, `src: url("<stem>-<style>.woff2") format("woff2")`, and `font-display: swap`.
  - **WHEN** `fonts/fonts.css` is read, **THEN** its opening comment **SHALL** say that the file is offered under `MIT OR Apache-2.0`, that the fonts it names are offered under the SIL Open Font License 1.1, and that the file is made by the tool.
  - **WHEN** `fonts/fonts.css` differs from what the list gives, **THEN** `css --check` **SHALL** exit non-zero, name the file, and change nothing.
  - **WHEN** a font the list calls for is missing from `fonts/`, **THEN** `css` and `css --check` **SHALL** exit non-zero and name the missing file.
  - **WHEN** `css` is run twice, **THEN** the two results **SHALL** be byte-identical, with line feeds for line ends.
- **Notes:** this task owns the one reader of `families.toml` that every later command uses.

### T-005: Write and check the manifest of checksums
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)
- **Touches:** src/ (the `manifest` and `check` commands), fonts/manifest.toml, tests/
- **Depends on:** T-003, T-004
- **Acceptance criterion:** INT-0002 criterion 5, "A manifest records, for every font file, its SHA-256 and its size, and which build of Cruor the files came from. A check fails if a font file and the manifest disagree".
- **Success criterion (EARS):**
  - **WHEN** `manifest --source-commit <id>` is run with a full commit id of forty hexadecimal characters, **THEN** `fonts/manifest.toml` **SHALL** record that commit and, for each of the thirty-two fonts, its file name, its size in bytes and its SHA-256.
  - **WHEN** `--source-commit` is given anything but forty hexadecimal characters, or `manifest` is run with no commit given and none recorded, **THEN** it **SHALL** exit non-zero and write nothing.
  - **WHEN** a font's bytes differ from the manifest, **THEN** `manifest --check` **SHALL** exit non-zero and name the file.
  - **WHEN** a font the list calls for is missing from `fonts/`, or `fonts/` holds a `.woff2` the list does not call for, **THEN** `manifest --check` **SHALL** exit non-zero and name it.
  - **WHEN** `manifest` is run without `--source-commit` and a manifest exists, **THEN** it **SHALL** keep the commit already recorded.
  - **WHEN** `check` is run, **THEN** it **SHALL** run `css --check` and `manifest --check` and exit non-zero if either fails.
- **Notes:** the manifest is written once with the commit noted in T-003. It uses T-004's reader of the list.

### T-006: Check that each font agrees with its rule
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)
- **Touches:** tools/check_fonts.py, tools/run-guards.sh, tests/
- **Depends on:** T-004
- **Acceptance criterion:** INT-0002 criterion 5, "or if a font's own name for its family and style disagrees with its `@font-face` rule".
- **Success criterion (EARS):**
  - **WHEN** `python -I tools/check_fonts.py fonts` is run and every font's own family name, style name, weight and slant agree with its family in `families.toml` and its rule in `fonts.css`, **THEN** it **SHALL** exit 0.
  - **WHEN** any font disagrees with its family or its rule, **THEN** it **SHALL** exit non-zero and name the file and the field that disagrees.
  - **WHEN** `bash tools/run-guards.sh` is run, **THEN** it **SHALL** also run `tools/check_fonts.py` on `fonts/` and exit non-zero if it fails.
- **Notes:** reads the fonts with fontTools. Takes the folder as its argument, so a test can point it at a copy with two fonts swapped.

### T-007: Make a page that sets a line in every face
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)
- **Touches:** fonts/specimen.html, tests/
- **Depends on:** T-004
- **Acceptance criterion:** INT-0002 criterion 4, "a page that links that stylesheet loads each of the thirty-two faces and sets text in it"; and it is where criterion 3's "a page asking a family for its bold or its italic is given that file" is seen in a browser.
- **Success criterion (EARS):**
  - **WHEN** `fonts/specimen.html` is opened over HTTP in a browser, **THEN** it **SHALL** load `fonts.css` by relative address and show one labelled line in each of the thirty-two faces, each asked for by family, weight and style, with each line's label and its sample sentence in separate elements; and a face asked for alone by family, weight and style **SHALL** be answered by its own `.woff2` and no other.
  - **WHEN** `fonts/specimen.html` is read, **THEN** it **SHALL** hold no script, and every address in it **SHALL** be the bare name of a file in `fonts/`.
- **Notes:** a plain page, black on white. It is not the look, and it is not part of a release.

### T-008: Put a release together with one command
- **Intent:** [INT-0005](../../../intents/INT-0005-versioned-releases.md)
- **Touches:** src/ (the `bundle` command), tests/
- **Depends on:** T-002, T-004, T-005
- **Acceptance criterion:** INT-0005 criteria 1, 2 and 3.
- **Success criterion (EARS):**
  - **WHEN** `bundle --out <dir>` is run on a clean checkout, **THEN** `<dir>` **SHALL** hold, with no folders, the thirty-two fonts, `fonts.css`, `OFL.txt`, `LICENSE-MIT`, `LICENSE-APACHE`, `manifest.json`, the archive `cruor-framework-v<version>.zip` holding every one of those files, and `cruor-framework-v<version>.zip.sha256` giving the archive's SHA-256.
  - **WHEN** `manifest.json` is read, **THEN** it **SHALL** give the framework's version (the crate's), the commit of Cruor recorded in `fonts/manifest.toml`, and for each of the fonts, `fonts.css`, `OFL.txt` and the two code licences its name, its size in bytes and its SHA-256.
  - **WHEN** `bundle` is run twice at the same commit, **THEN** `manifest.json`, the archive and the archive's checksum file **SHALL** be byte-identical between the two.
  - **WHEN** `css --check` or `manifest --check` would fail, **THEN** `bundle` **SHALL** exit non-zero and write nothing.
  - **WHEN** the bundle's `fonts.css` is read, **THEN** every address in it **SHALL** be a bare file name that is present in `<dir>`.
  - **WHEN** `<dir>` exists and is not empty, **THEN** `bundle` **SHALL** exit non-zero and write nothing.
  - **WHEN** `bundle --out <dir> --tag <tag>` is run and the tag is not `v` followed by the crate's version, **THEN** it **SHALL** exit non-zero and write nothing.
- **Notes:** the archive is made the same every time: entries in name order, one fixed timestamp. The bundle takes exactly the files the list and this task name, so nothing stray in the working folder can enter a release. The manifest cannot list the archive, which holds the manifest; the archive has its own checksum file instead (INT-0005 criterion 1).

### T-009: Show a build fetching a release and checking it
- **Intent:** [INT-0005](../../../intents/INT-0005-versioned-releases.md)
- **Touches:** examples/fetch-release.mjs, tests/
- **Depends on:** T-008
- **Acceptance criterion:** INT-0005 criterion 4, "A build that fetches a release's files over HTTP and checks each against the manifest ends with files identical to the repository's", and the showing of it that criterion 6 asks of the README.
- **Success criterion (EARS):**
  - **WHEN** `node examples/fetch-release.mjs <address> <dir>` is run against an address that serves a bundle, **THEN** it **SHALL** fetch `manifest.json` and every file it lists into `<dir>`, and **SHALL** exit 0 only if each file's size and SHA-256 agree with the manifest.
  - **WHEN** a fetched file disagrees with the manifest, **THEN** it **SHALL** exit non-zero, name the file, and leave no copy of that file in `<dir>`.
  - **WHEN** the manifest lists a name that is not a bare file name, **THEN** it **SHALL** exit non-zero before fetching any file.
  - **WHEN** it is given `--manifest-sha256 <value>` and the fetched `manifest.json` has another SHA-256, **THEN** it **SHALL** exit non-zero before fetching any file.
  - **WHEN** the address cannot be reached, **THEN** it **SHALL** exit non-zero and name the address.
- **Notes:** no dependencies; runs on Node 20 or newer. It is an example a page's build can copy, not a part a page must use. A build that pins the manifest's SHA-256 beside the version gets exactly the files it expects; without it the check shows only that the files and the manifest agree with each other. A real release's address answers with a redirect, which the local tests do not meet; the release's own check (T-010) is where that is first exercised.

### T-010: Publish a release when a version tag is pushed
- **Intent:** [INT-0005](../../../intents/INT-0005-versioned-releases.md)
- **Touches:** .github/workflows/release.yml, tools/release-gate.sh, tests/
- **Depends on:** T-001, T-008, T-009
- **Acceptance criterion:** INT-0005 criterion 5.
- **Success criterion (EARS):**
  - **WHEN** a tag beginning `v` is pushed, **THEN** `release.yml` **SHALL** run the guards, run `bundle` with that tag, and publish a release for the tag holding every file in the bundle's folder.
  - **WHEN** the tagged commit is not on `main`, or a release for the tag already exists, or the guards or the bundle fail, **THEN** `release.yml` **SHALL** fail and publish nothing.
  - **WHEN** `tools/release-gate.sh <tag>` is run, **THEN** it **SHALL** exit 0 only if the tagged commit is an ancestor of `origin/main` and no release, draft or public, exists for the tag; otherwise it **SHALL** exit non-zero and say which, naming a draft left behind so the owner can remove it.
  - **WHEN** `release.yml` publishes, **THEN** it **SHALL** make the release as a draft, add every file, and only then make it public, so that no release is public with files missing.
  - **WHEN** the release is public, **THEN** `release.yml` **SHALL** run `examples/fetch-release.mjs` against the release's own address, pinned to the SHA-256 of the manifest it built, and **SHALL** fail if that does not exit 0.
  - **WHEN** that check of the public release fails, **THEN** `release.yml` **SHALL** return the release to a draft before it fails, so that nothing stays public that has not proven itself, and **SHALL** say that the draft is left for the owner.
- **Notes:** only `release.yml` is given leave to write to the repository, and only for publishing the release. No tag is pushed in this sprint: the first, `v0.1.0`, waits for the owner's word after this sprint's pull request is merged. The first run of this workflow is therefore also the first real release; the clauses above are what keep a wrong or repeated tag from publishing. A protected environment with a required reviewer was considered and not taken: it is a setting of the repository the owner would have to keep, and tags are pushed only on the owner's word (INT-0005, Alternatives). The workflow never deletes a release: a draft left by a failed run is the owner's to remove before the tag is tried again, and backlog task T-102 records what was done if that happens. The two gates live in `tools/release-gate.sh` so they can be tested for real, against a scratch repository and a stand-in for the GitHub client.

### T-011: Write the README
- **Intent:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)
- **Touches:** README.md, tests/
- **Depends on:** T-007, T-008, T-009
- **Acceptance criterion:** INT-0001 criteria 1 and 3; [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) criterion 2, "the README says the fonts are offered under it"; and [INT-0005](../../../intents/INT-0005-versioned-releases.md) criterion 6.
- **Success criterion (EARS):**
  - **WHEN** the README is read, **THEN** it **SHALL** say what the kit is, name the look Cruentous Atonement, and say that the look is not in the kit yet.
  - **WHEN** the README is read, **THEN** it **SHALL** list the eight families by name and the four styles each has.
  - **WHEN** the README is read, **THEN** it **SHALL** show a page linking `fonts.css` and setting text in a named family.
  - **WHEN** the README is read, **THEN** it **SHALL** say that a family's bold and italic are asked for by `font-weight` and `font-style`, and that in a name such as "Cruor Sans Regular" the last word is part of the family's name.
  - **WHEN** the README is read, **THEN** it **SHALL** give the address pattern `https://github.com/crussella0129/cruor-framework/releases/download/v<version>/<file>`, show a build fetching and checking a release with `examples/fetch-release.mjs`, and say that a build should pin the manifest's SHA-256.
  - **WHEN** the README is read, **THEN** it **SHALL** say what running the checks requires: the Rust toolchain the repository pins, Python with the packages of `tools/requirements.txt`, the browser Playwright drives, and Node 20 or newer.
  - **WHEN** the README is read, **THEN** it **SHALL** say that the fonts are offered under the SIL Open Font License 1.1 with the name Cruor reserved, that `fonts/OFL.txt` is what states the fonts' terms, and that the code is offered under `MIT OR Apache-2.0`, naming the three licence files.
  - **WHEN** each file path and each command the README names is looked up, **THEN** the path **SHALL** exist and the command **SHALL** be one the tool has.
- **Notes:** the README describes Cruor in its own terms, as every file here does.

### T-012: Bundle in CI on every push and keep the result
- **Intent:** [INT-0005](../../../intents/INT-0005-versioned-releases.md)
- **Touches:** .github/workflows/ci.yml, tests/
- **Depends on:** T-001, T-008
- **Acceptance criterion:** INT-0005 criterion 2, "The same commit always gives the same manifest", seen across two machines; and it rehearses the bundling half of criterion 5 on every push.
- **Success criterion (EARS):**
  - **WHEN** a commit is pushed to `main` or `dev`, or a pull request is opened, **THEN** CI **SHALL** run `bundle` and keep its folder as a build artefact.
  - **WHEN** `ci.yml` is read, **THEN** it **SHALL** ask for no leave to write to the repository.
- **Notes:** the artefact's `manifest.json` is compared in the Test phase with one made on another machine at the same commit.

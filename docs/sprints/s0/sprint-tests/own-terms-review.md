# The own-terms review: a record

[INT-0001](../../../intents/INT-0001-the-cruor-framework.md) criterion 5:
nothing in this repository or its history names another typeface or
describes Cruor by comparison with one. Task T-013 keeps that by a review
made before every push, from outside the repository, because a check kept
here would have to hold the names it forbids.

How each review is made:

- For every commit not yet pushed, the content of every file the commit
  adds or changes, the file's path and the commit's message are searched
  for the names of other typefaces. The list of names is kept outside the
  repository.
- Font files are opened with fontTools. Every string of each font's name
  table and every glyph name is searched, and each font's WOFF2 metadata
  block and private block is read, or noted as absent.
- The new prose of those commits is read once for any description of Cruor
  by comparison with another typeface. Lines holding the words that usually
  mark a comparison are picked out for that reading.
- The files each commit adds or changes are set against what the commit's
  task touches.
- A commit whose only change is a new entry in this file is covered by the
  entry it adds.

## Entries

### 1. 23 November 2026, before the first push of Build

- **Commits covered:** `163b32002e9f7c745d6a265b2e37279d00cb720b` to
  `1b91c7e341f44c302d221c0a47e1d61fe0530ab2`, six commits: T-001, T-002 and
  T-003, each with its commit of evidence. The commits before them were
  searched before they were pushed, in the Research and Plan phases.
- **Also covered:** the thirty-two font files of T-003, opened with
  fontTools: every name-table string and every glyph name. No font has a
  WOFF2 metadata block or a private block (both lengths are zero in all
  thirty-two).
- **Found:** none.
- **Read for comparisons:** two lines were picked out, both the same line of
  `LICENSE-APACHE` ("based on (or derived from) the Work"), which is the
  licence's own wording. Nothing describes Cruor by comparison.
- **Files against tasks:**
  - T-001 (`163b320`): `.gitattributes`, `.github/workflows/ci.yml`,
    `.gitignore`, `Cargo.lock`, `Cargo.toml`, `pyproject.toml`,
    `rust-toolchain.toml`, `src/main.rs`, `tools/requirements.txt`,
    `tools/run-guards.sh` and five files under `tests/`: all in the task's
    Touches. Also the Book's two ledgers and INT-0002, for its move to
    `active`.
  - T-002 (`6d3fdc9`): `LICENSE-MIT`, `LICENSE-APACHE`, `Cargo.toml`,
    `tests/test_licences.py`: all in the task's Touches. Also the two
    ledgers and INT-0001, for its move to `active`.
  - T-003 (`d4fdcfe`): the thirty-two `.woff2` files, `fonts/OFL.txt`,
    `fonts/families.toml`, `tests/test_fonts_intake.py`: all in the task's
    Touches. Also the two ledgers.
  - The three commits of evidence change `docs/work/completed-tasks.md`
    alone.
  - Nothing is unaccounted for. No file from the Cruor project is in the
    repository but the thirty-two fonts.
- **The intake (T-003):**
  - The fonts were built from the Cruor project at commit
    `777120960fd302eb565806badf18a87b49beeffb`, the head of its working
    branch at the time, in a copy made for the purpose outside both
    repositories. The copy's tree had nothing uncommitted. Only the
    thirty-two `.woff2` files were copied from the build's output.
  - Against `font-inventory.md`: the eight family names agree, the four
    styles and their weights (400 and 700) agree, and the glyph counts agree
    (328 in each proportional font, 779 in each Mono and Pixelated font).
  - Differences from the inventory: thirty-one of the thirty-two files
    differ in size from the build the inventory was read from, by between
    96 bytes fewer and 116 bytes more, 768,080 bytes in all against
    768,324. Table by table, the fonts of the two builds differ only in
    `head`, which holds the time a font was made; every outline, name and
    measure is the same. The sizes differ because the files are compressed.
  - The licence file's text is the SIL Open Font License 1.1 as its authors
    publish it, beneath the copyright line of INT-0002 criterion 2. The
    Apache License's text is the published one, byte for byte.

### 2. 23 November 2026, before the second push of Build

- **Commits covered:** `ff5eebf15500bba9090599cd3309655368f33f86` to
  `446ceb5cc8418d1252d3af70f845013f725fd499`, three commits: T-004 with its
  commit of evidence, and a correction to CI. The two commits that recorded
  entry 1 (`03ad441`, `7c97e55`) were searched with the same list before
  the first push; none was found in them.
- **Also covered:** nothing; no font file is among these commits.
- **Found:** none.
- **Read for comparisons:** no line was picked out. The stylesheet's
  comments say of each family only how its characters are set.
- **Files against tasks:**
  - T-004 (`ff5eebf`): `src/main.rs`, `src/families.rs`, `src/css.rs`,
    `fonts/fonts.css`, `tests/common/mod.rs`, `tests/css.rs`: all in the
    task's Touches. Also the two ledgers.
  - `446ceb5` changes `.github/workflows/ci.yml` alone and belongs to no
    task. The first CI run stopped before any check, because the hosted
    runner's latest Ubuntu is newer than the pinned browser driver knows;
    the workflow now names the release of Ubuntu it runs on. It is a
    correction to T-001's work, found by running it.

### 3. 23 November 2026, before the third push of Build

- **Commits covered:** `a6587d99dd6f99ce9051c21d6d554a804218f4a5` to
  `a5969e5d98445fc4472d7096c3a8f86f05206f79`, sixteen commits: T-005 to
  T-012, each with its commit of evidence. The commit that recorded entry 2
  (`db6fad0`) changes this file alone.
- **Also covered:** nothing; no font file is among these commits.
- **Found:** none.
- **Read for comparisons:** no line was picked out. The new prose is the
  README, the specimen page, the fetch example and the comments of the tool
  and the workflows. The README says of Cruor that its letters are tall and
  narrow with ornament of their own, and describes each family by what its
  letters carry; nothing is said by comparison.
- **Files against tasks:**
  - T-005 (`a6587d9`): `src/main.rs`, `src/manifest.rs`,
    `fonts/manifest.toml`, `tests/manifest.rs`.
  - T-006 (`da7b5f5`): `tools/check_fonts.py`, `tools/run-guards.sh`,
    `tests/test_check_fonts.py`, `tests/test_guards.py`.
  - T-007 (`4e0bd53`): `fonts/specimen.html`, `tests/test_specimen.py`.
  - T-008 (`9f1b755`): `src/main.rs`, `src/bundle.rs`, `tests/bundle.rs`,
    and INT-0005, for its move to `active`.
  - T-009 (`cfee3a0`): `examples/fetch-release.mjs`,
    `tests/test_fetch_release.py`, `tests/helpers.py`,
    `tests/test_specimen.py`. The last two gained and took up one shared
    way of serving a folder to the tests.
  - T-010 (`82ce34c`): `.github/workflows/release.yml`,
    `tools/release-gate.sh`, `tests/test_release.py`.
  - T-011 (`8c8938c`): `README.md`, `tests/test_readme.py`.
  - T-012 (`88a7f9f`): `.github/workflows/ci.yml`, `tests/test_ci.py`.
  - Each is in its task's Touches, with the Book's two ledgers beside it.
    The eight commits of evidence change `docs/work/completed-tasks.md`
    alone. Nothing is unaccounted for, and no file from the Cruor project
    was added.

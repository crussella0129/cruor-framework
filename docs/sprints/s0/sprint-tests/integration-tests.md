# Sprint 0 Integration Test Results

- **Tested commit:** `49dd8934f7f04f721504e7cbd0ef2c1d45209ccf`, the head of
  `dev` when the checks were made, in a fresh clone with nothing
  uncommitted.
- **The same commit in CI:** run
  [45266754572](https://github.com/crussella0129/cruor-framework/actions/runs/45266754572)
  on Ubuntu 24.04, conclusion `success`.
- The unit record beside this one, [unit-tests.md](unit-tests.md), gives the
  guard script's confirmations step by step.

The checks were made four times, and this page gives the fourth:

1. At `6c9fb0b1cdd37a9e683d15bf6385a47b1060a565`, the head the Build left.
   Every automated test passed, and the reading of the README found one
   fault, told below under "The README, read". It was corrected in
   `27fc856bb4e47fcbf63fc1ab786c03e5ace6b6b1`.
2. At `3b7b3d34de3f6ef75b61a912a06b6ce67525c917` (CI run
   [45262447194](https://github.com/crussella0129/cruor-framework/actions/runs/45262447194),
   `success`). Everything passed. The phase's first critique was made of
   that evidence ([critique-round-1.md](critique-round-1.md)) and found
   tests that held their clauses loosely and one remark here that said too
   little. The tests were tightened and added to in
   `3ab351acdc88b786eabaa22e68ccc54cbdfe0b62`, which changes tests alone.
3. At `acee815beae9dacdfd6d8e72ea318b29ae08d2a5` (CI run
   [45265330443](https://github.com/crussella0129/cruor-framework/actions/runs/45265330443),
   `success`). Everything passed. The second critique
   ([critique-round-2.md](critique-round-2.md)) found that two tests of the
   workflows matched the guard and bundle commands by a part only, and
   that two sentences on this page said slightly more than the evidence.
   The tests were tightened in `c2c6a8bfa75bc8e1fe4ab90b0f85fb606ebf20da`,
   which changes tests alone, and the sentences are reworded below.
4. At the tested commit, where everything on this page was made again.

## The repository as it stands
- **Intents:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md), [INT-0005](../../../intents/INT-0005-versioned-releases.md)

| Test | Result | Evidence |
|---|---|---|
| `repository_passes_check` | passed | `tests/manifest.rs`, in the guard run at the tested commit: `check` exits 0 on the tracked files |
| `ci_guards_green_on_dev` | passed | run 45266754572, head `49dd893`: the step "Guards", which runs `bash tools/run-guards.sh`, concluded `success`, as did every other step |
| `ci_bundle_matches_local` | passed | the artefact `cruor-framework-bundle` of that run, set against a bundle made in a fresh clone on the owner's machine at the same commit |

`ci_guards_green_on_dev`, more exactly: the run is for the last commit on
`dev` when the tests were made. The commits that record these results come
after it and change the Book alone. Their own CI run cannot be written
into the commit it runs on; it is read at the Loop phase, before the pull
request is opened.

`ci_bundle_matches_local`, more exactly: CI's bundle was made on Linux, the
other on Windows 11 with `cargo run --release -- bundle --out dist`. Each
holds thirty-nine files, and all thirty-nine are byte-identical between
the two, the archive among them.

- `manifest.json`, SHA-256
  `6fe8d4b22f83d1a2491b30683cb10a8f196ed58546de01aaf3ce2c4298472ff6` in both.
- `cruor-framework-v0.1.0.zip`, SHA-256
  `12e32d887e1b28e2e44eea751328232753f83b716c8f5ab24893bb6ec4d8a576` in both,
  and it is the value the archive's own checksum file gives.

The same two values were found at `6c9fb0b` (CI run
[45246763880](https://github.com/crussella0129/cruor-framework/actions/runs/45246763880)),
at `3b7b3d3` and at `acee815`: the commits between changed the README and the tests,
which are not part of a release. CI keeps its artefact for thirty days;
after that these recorded values are what remains of the comparison.

## The reviews of T-013
- **Intents:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md), [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)
- **The record read:** [own-terms-review.md](own-terms-review.md), entries 1
  to 6, as it stood at the tested commit.

| Test | Result |
|---|---|
| `review_own_terms_before_each_push` | **met after the fact for three pushes, not before them**: a deviation, told below. Nothing was found in any search |
| `review_font_name_tables` | passed |
| `review_pull_request_text` | not yet due: the Loop phase makes it, before the pull request is opened |
| `review_updater_pull_requests` | passed: there is no pull request to review |
| `review_commits_touch_only_their_tasks` | passed |
| `review_intake_matches_inventory` | passed |
| `review_record_is_complete` | passed for the pushes since the record began; the same deviation applies |

### `review_own_terms_before_each_push`

`dev` has been pushed eight times. The last six pushes each have an entry
made before them, and every entry's number found is none:

| Push, by the head it left on `dev` | Entry | Commits in the entry's range |
|---|---|---|
| `7c97e55` | 1 | `163b320` to `1b91c7e`, six |
| `db6fad0` | 2 | `ff5eebf` to `446ceb5`, three |
| `6c9fb0b` | 3 | `a6587d9` to `a5969e5`, sixteen |
| `3b7b3d3` | 4 | `27fc856`, one; and the whole history again, thirty-four |
| `acee815` | 5 | `3ab351a`, one |
| `49dd893` | 6 | `c2c6a8b`, one |

`dev` held thirty-nine commits at the tested commit. The history was read
from git for this test and each commit set against the record:

- Twenty-eight fall in the ranges of entries 1 to 6.
- Five change the record alone and are covered by the entry they add:
  `db6fad0`, `6c9fb0b`, `3b7b3d3`, `acee815` and `49dd893`.
- Six fell in no range before the Test phase: the four of the Research and
  Plan phases (`7832759`, `165d4a1`, `90bd2f1`, `6f2c638`) and the two that
  recorded entry 1 (`03ad441`, `7c97e55`). Entry 4 covers them: it searched
  the whole history from the first commit to `27fc856` with the same list
  and found none.

**The deviation.** The test plan asks for an entry made before every
push. Three pushes went out with commits that no entry covered at the
time:

- The two pushes of the Research and Plan phases, which left `165d4a1` and
  then `6f2c638` at the head of `dev`. They were made before the record
  existed, because the plan that sets the review up was written in those
  phases.
- The first push of the Build, which left `7c97e55`. Entry 1 was made
  before it, but the push also carried `03ad441` and `7c97e55`, which
  entry 1's range does not hold. `03ad441` adds entry 1 and also moves
  T-013 between the Book's two ledgers, so it is not a commit whose only
  change is a new entry.

Those six commits were searched before they were pushed, but nothing made
at the time shows it: entries 1 and 2 only say so afterwards, each for its
own commits (entry 1 for the four of the Research and Plan phases, entry 2
for the two that recorded entry 1). What the record does
show is entry 4, which searched the whole history with the list and found
none, and the critic's own search of every commit with a list of its own,
which also found none. So the clause is met after the fact for these three
pushes and not before them, and nothing was made public that the rule
forbids. Since entry 2, every push has had its entry first.

### `review_font_name_tables`

Entry 1 covers T-003's commit (`d4fdcfe`) and says that every name-table
string and every glyph name of the thirty-two fonts was read with fontTools
and searched, and that no font has a WOFF2 metadata block or a private
block. Number found: none. Entry 4 repeats the reading with the same
result.

### `review_updater_pull_requests`

GitHub lists no pull request for the repository, open or closed (asked
again at the tested commit, and recorded in entries 4, 5 and 6). The dependency updater is set
to look at the workflows weekly and open its pull requests against `dev`;
its one run so far, at `165d4a1`, ended in failure and opened nothing; no
workflow file existed then. The Loop phase asks again before the sprint's pull request
is opened.

### `review_commits_touch_only_their_tasks`

For this test the files each of the thirty-nine commits adds or changes
were listed from git and set against the entries. Every entry's list
agrees with git, each task's files are within the task's Touches, and the
Book's ledgers and records are accounted for as such. Four commits
belong to no task and are accounted for in entries 2, 4, 5 and 6: the
correction to CI (`446ceb5`), the correction to the README (`27fc856`) and
the two tightenings of the tests (`3ab351a`, `c2c6a8b`). Entry 4 also
accounts for the two files outside the Book that the commits before the
Build change, `.github/dependabot.yml` and `.gitignore`. The only files
from the Cruor project are the thirty-two fonts.

One thing the reading turned up outside the record: the completed-tasks
ledger's entry for T-002 lists `Cargo.lock` among the files modified, and
T-002's commit (`6d3fdc9`) does not change that file. The review's entry is
right and the ledger's line is not. The ledger is append-only, so the
difference is noted here and in the test report.

### `review_intake_matches_inventory`

Entry 1 gives the commit of Cruor that was built,
`777120960fd302eb565806badf18a87b49beeffb`, in full. It is the commit
`fonts/manifest.toml` records. The entry says the build's tree had nothing
uncommitted, and sets the eight family names, the four styles and their
weights, and the glyph counts (328 and 779) against `font-inventory.md`:
all agree. The one difference it records is in file sizes, and it is
explained: the two builds differ only in the table that holds the time a
font was made.

### `review_record_is_complete`

The whole record was read. Every entry gives its date, its first and last
commit, what else it covered and its number found, which is none in all
six. Nothing was found, so no entry had anything to dispose of. Every
push since the record began has an entry; the deviation told above, about
the two pushes before it began and the two commits the first entry's range
left out, applies here too.
The entries for the pushes that close the sprint and open its pull request
are added and read at the Loop phase, as the test plan says.

## The README, read
- **Intent:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)

`review_readme_against_checklist`: **passed at the tested commit, after one
correction.** The README was read at `6c9fb0b` and again after the
correction; it has not changed since `27fc856`, and the commands and the
page below were run again at the tested commit.

| Item of the checklist | At `6c9fb0b` | At the tested commit |
|---|---|---|
| Every command shown was run as written and did what the README says | met, but for the one below that cannot be yet | the same |
| The example page, saved and opened, shows its text in the family it names | not made | met |
| The address pattern, filled in, has the form GitHub documents | met | met |
| Nothing is said of the look beyond its name and that it is to come | **not met** | met |

### The commands

Run in a fresh clone of `dev` at the tested commit, outside the
repository's folder:

| Command, as the README writes it | What happened |
|---|---|
| `cargo run --release -- css` | exit 0 |
| `cargo run --release -- manifest` | exit 0; after this and the one before, git reports no tracked file changed: both files were already as the tool writes them |
| `cargo run --release -- check` | exit 0 |
| `cargo run --release -- bundle --out dist` | exit 0; `dist` holds thirty-nine files and no folder: the thirty-two fonts, `fonts.css`, `OFL.txt`, `LICENSE-MIT`, `LICENSE-APACHE`, `manifest.json`, the archive and its checksum file, which is what the README says a release holds |
| `bash tools/run-guards.sh` | exit 0, in the same clone before any other command; git reported nothing untracked or changed after it (the unit record gives its steps) |
| `python -m playwright install chromium` | exit 0, on a machine that already had the browser |
| `node examples/fetch-release.mjs https://github.com/crussella0129/cruor-framework/releases/download/v0.1.0/ <folder> --manifest-sha256 <value>` | exit 1, saying `cannot fetch …/v0.1.0/manifest.json: HTTP 404`, and nothing written: there is no release yet |

The last command cannot do what the README shows until `v0.1.0` is
published; what it did is what the README says the example does when a file
cannot be fetched. The same command was then given the address of that
bundle served over HTTP on this machine, with the SHA-256 of its
`manifest.json` pinned: exit 0, "36 files of cruor-framework 0.1.0 fetched
into public/fonts and checked", and the folder held those thirty-six files
and `manifest.json`, each identical to the bundle's. The run against the
real address is `release_checks_itself_v0_1_0`, not yet possible
([e2e-tests.md](e2e-tests.md)).

The README's sentence "The same commit gives the same bytes every time" is
what `ci_bundle_matches_local` shows, above.

### The example page

The README's page links `fonts/fonts.css`, so it was saved beside a copy of
the folder `fonts/`, not inside it, with the README's block as its head and
a heading, a paragraph with a `<strong>` and an `<em>`, and a `<code>` as
its body. It was served over HTTP on this machine and opened in headless
Chromium.

- The browser fetched five font files and no others:
  `CruorThornamentalRegular-Bold.woff2` for the heading,
  `CruorLiteRegular-Regular.woff2`, `CruorLiteRegular-Bold.woff2` and
  `CruorLiteRegular-Italic.woff2` for the paragraph, and
  `CruorSansMono-Regular.woff2` for the code. That is the README's
  sentence about `<h1>`, `<strong>` and `<em>`, seen.
- The five faces report as loaded. No request failed and none left the
  machine.
- Each piece of text measures a different width in the family the page
  names than in the plain fallback the page gives after it. For the
  italic the two differ by about a tenth of a pixel in a short phrase,
  which is why the files fetched and the faces loaded are the proof and
  the widths only stand beside it.
- A picture of the page was taken and looked at: the heading, the
  paragraph with its bold and its italic, and the code are all in Cruor.

### The address pattern

Filled in with the version `0.1.0` and the file `fonts.css`, the pattern
gives
`https://github.com/crussella0129/cruor-framework/releases/download/v0.1.0/fonts.css`.
The form is `https://github.com/<owner>/<repository>/releases/download/<tag>/<file>`,
which is the address GitHub's own interface reports for a file of a public
release (read from the latest release of GitHub's command-line client).

### What is said of the look

At `6c9fb0b` the README's first sentence read "A kit that gives a web page
the look called **Cruentous Atonement**: blood letters cut into obsidian,
set in Cruor." The words after the colon say what the look is, which the
checklist does not allow before the look is in the kit. `27fc856` took
them out. At the tested commit the README says of the look its name, the
Latin the name comes from, that it "is not in the kit yet", and that its
colours, its stylesheet and its theme file are "what is built next".

Two things in that are a judgement, and it is made here. The first
sentence still ends "set in Cruor": that is read as saying which typeface
the kit holds, which is in the kit today, and not as a description of the
look. And naming the look's three parts is read as part of saying that it
is to come, since they are named only as what is built next. A new test,
`test_readme_says_of_the_look_only_its_name`, now holds the paragraph that
first names the look, whole, so the words taken out cannot come back to
that paragraph unnoticed; the sprint that builds the look changes that
test with the README. The test holds that one paragraph and no other: a
description of the look added anywhere else in the README would pass it,
so the rest of this item stays a reading at each sprint.

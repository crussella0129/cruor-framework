# Sprint 0 Test Report

Sprint 0 took in Cruor's thirty-two web fonts and built the path that
releases them. On the tested commit every automated test passes, on the
owner's machine and in CI, and CI's bundle is byte-identical to one made
here. Two things were corrected on the way and one promise of the test
plan was kept late; all three are told under "Failures" below. One proof
cannot be made until the first release exists.

The records this report draws on are beside it:
[unit-tests.md](unit-tests.md), [integration-tests.md](integration-tests.md),
[e2e-tests.md](e2e-tests.md), [own-terms-review.md](own-terms-review.md),
and the three critiques, [critique-round-1.md](critique-round-1.md),
[critique-round-2.md](critique-round-2.md) and [critique.md](critique.md).

## Intent Verification
| Intent | Acceptance criterion | EARS / tests | Result | Intent evidence update |
|--------|----------------------|---------------|--------|------------------------|
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 1: thirty-two `.woff2`, named by family and style | T-003 / `test_fonts_are_the_thirty_two`, `test_families_list_has_eight` | pass | Test evidence links this report |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 2: the licence beside the fonts with the copyright line; the README says the fonts are under it | T-003, T-011 / `test_ofl_text_and_copyright_line` (now holding the licence's whole text by its SHA-256), `test_readme_states_terms` | pass | Test evidence links this report |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 3: one stylesheet, four styles joined, a bold or an italic given its own file | T-004, T-007 / the six `css_*` tests; `test_specimen_fetches_a_file_for_each_face` (thirty-two cases) | pass | Test evidence links this report |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 4: a browser loads each of the thirty-two faces and sets text in it | T-007 / `test_specimen_loads_all_faces`, `test_specimen_styles_of_a_family_differ`, `test_specimen_is_not_in_a_fallback`, `test_specimen_is_self_contained` | pass | Test evidence links this report |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5: the manifest, and checks that fail when a font and the manifest, or a font and its rule, disagree | T-001, T-005, T-006, T-013 / the nine tests of `tests/manifest.rs`; the `test_check_fonts_*` tests, with two added for a font or a rule that names the wrong family; the guard and CI tests; `ci_guards_green_on_dev`; `review_intake_matches_inventory` | pass | Test evidence links this report |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 6: no other file from the Cruor project | T-003, T-013 / `test_no_other_font_files_tracked`, `review_commits_touch_only_their_tasks` | pass | Test evidence links this report. All six criteria are proven on `dev`. The intent's move to `realized` waits for the merge that brings the fonts to the default branch (see "Coverage Observations") |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 1: one command puts a release together | T-008 / `bundle_holds_expected_files`, `bundle_archive_holds_same_files`, `bundle_archive_checksum_is_right`, `bundle_manifest_matches_files`, `bundle_refuses_when_a_check_fails`, `bundle_refuses_nonempty_folder` | pass | Test evidence links this report |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 2: the same commit, the same manifest | T-008, T-012 / `bundle_is_reproducible`, `test_ci_workflow_keeps_bundle`, `test_ci_workflow_cannot_write`, `ci_bundle_matches_local` (all thirty-nine files identical between Linux and Windows) | pass | Test evidence links this report |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 3: relative addresses | T-008 / `bundle_css_addresses_are_bare_and_present` | pass | Test evidence links this report |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 4: a build that fetches and checks ends with identical files | T-009 / the five `test_fetch_release_*` tests of the plan, and `test_fetch_release_follows_a_redirect`, added | pass | Test evidence links this report |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 5: a pushed tag on `main` publishes, whole or not at all, never over a release, and the release proves itself | T-001, T-008, T-010 / `test_crate_version_is_first_release`; the two tag tests of `bundle`; the six tests that read `release.yml`, now holding its guard and bundle commands whole; the tests that run `tools/release-gate.sh` for real, now holding the question it asks; `release_checks_itself_v0_1_0` | **not yet proven**: everything short of a real release passes; the release's own check cannot run until `v0.1.0` is pushed | Test evidence links this report. Not eligible for `realized` until backlog task T-102 records that run |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 6: the README gives the address pattern and shows the fetch | T-011 / `test_readme_gives_release_address`, `test_readme_shows_fetch_example`, `review_readme_against_checklist` | pass; the example's own address does not answer yet (see "Technical Debt Identified") | Test evidence links this report |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 1: the public repository holds the Book and a README that says what the kit is, what is in it and how a page takes it in | T-011 / the `test_readme_*` tests, with one added that holds the paragraph naming the look; `review_readme_against_checklist` | pass on `dev`; **not yet true of the default branch** (see "Coverage Observations") | Test evidence links this report |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 3: both licences at the root; the README says which terms cover what | T-002, T-011 / `test_code_licences_present`, `test_crate_declares_licence`, `test_readme_states_terms` | pass | Test evidence links this report |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 5: nothing in the repository or its history names another typeface | T-013 / `review_own_terms_before_each_push`, `review_font_name_tables`, `review_updater_pull_requests`, `review_record_is_complete`; `review_pull_request_text` is made at the Loop phase | **met, with a deviation**: nothing was found in any search of the whole history, but for three pushes the review's entry came after the push, not before | Test evidence links this report. The intent stays `active`: criteria 2 and 4 wait for the look |

## Summary
- Unit tests: 74 passed / 0 failed / 74 total (63 the plan names, 11
  beyond it).
- Integration tests: 8 passed / 0 failed / 11 total. Of the other three,
  two are met with the deviation told below
  (`review_own_terms_before_each_push`, `review_record_is_complete`) and one
  is not yet due (`review_pull_request_text`, made at the Loop phase). One
  of the eight, `review_readme_against_checklist`, passed with one command
  that cannot yet do what the README shows, because the release it names
  does not exist (see "Technical Debt Identified").
- E2E tests: 10 passed / 0 failed / 10 total (9 the plan names, 1 beyond
  it). One more, `release_checks_itself_v0_1_0`, is not yet possible.
- CI status: green.

Counted by the guard script itself, which counts every case of a test
that runs for several inputs: `cargo test` 32 passed, `pytest` 91 passed.
All 73 automated tests the plan names are among them.

## CI Confirmation
- **Head SHA:** `49dd8934f7f04f721504e7cbd0ef2c1d45209ccf`
- **CI run:** 45266754572,
  <https://github.com/crussella0129/cruor-framework/actions/runs/45266754572>
- **Conclusion:** success
- **Confirmations:** CI runs `bash tools/run-guards.sh`, the repository's
  one guard script, on Ubuntu 24.04 with Python 3.13 and Node 20, then
  bundles and keeps the bundle. Every step concluded `success`; its log
  shows `cargo test` as 32 passed and `pytest` as 91 passed. The same
  script was run at the same commit in a fresh clone on the owner's machine
  (Windows 11, Node 24.12.0) and exited 0 with the same totals;
  [unit-tests.md](unit-tests.md) gives its steps one by one. The bundle CI
  kept and the bundle made in that clone are identical in all thirty-nine
  files ([integration-tests.md](integration-tests.md)).

The commits that record this report come after the tested commit and
change the Book alone. Their CI run cannot be written into the commit it
runs on; the Loop phase reads it before the pull request is opened.

## Failures
No test fails on the tested commit. The phase found three things on the
way, and they are part of the result:

1. **The README said what the look is.** The plan's reading of the README
   allows the look's name and that it is to come. The first sentence went
   on to describe it. Affected: [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)
   criterion 1, by way of `review_readme_against_checklist`. Corrected in
   `27fc856`; a test now holds the paragraph whole.
2. **Some tests held their clauses loosely.** The first critique found
   that no test made a font disagree about its family, that the stand-in
   for the GitHub client would answer any question, that the licence's
   body and the search for carriage returns were checked more weakly than
   their clauses say, and that a redirect could be met locally. The second
   found that the tests of the two workflows matched the guard and bundle
   commands by a part only. None hid a fault: every tightened and added
   test passed against unchanged code. Affected:
   [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) criteria 2 and
   5, [INT-0005](../../../intents/INT-0005-versioned-releases.md) criteria 4
   and 5. Done in `3ab351a` and `c2c6a8b`, which change tests alone. The
   checks were therefore made four times, at `6c9fb0b`, `3b7b3d3`, `acee815`
   and the tested commit, and CI was green at each.
3. **A deviation from the test plan: three pushes went out before their
   review had an entry.** The plan asks for an entry in the own-terms
   record before every push. The two pushes of the Research and Plan
   phases were made before the record existed, and the first push of the
   Build carried two commits that its entry's range did not hold. The six
   commits concerned were searched at the time with nothing kept to show
   it. Entry 4 of the record later searched the whole history and found
   none, and the critic searched every commit with a list of its own at each of
   its three readings and found none. Affected: [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)
   criterion 5, which is met in substance (nothing in the history names
   another typeface) though the promised order was not kept for those
   three pushes. Every push since has had its entry first.

## Technical Debt Identified
- [INT-0005](../../../intents/INT-0005-versioned-releases.md) — the release
  workflow has never run. Its first run is the first real release, on the
  owner's word after the pull request is merged; backlog task T-102 records
  it. Until then no test has seen GitHub's own answer for a draft release,
  or a release's files as GitHub serves them.
- [INT-0005](../../../intents/INT-0005-versioned-releases.md) — the README's
  worked example names the address of `v0.1.0`, which answers HTTP 404
  until that release exists. The command as written was run and failed as
  the README says the example does when a file cannot be fetched; given
  the same bundle served on this machine it fetched and checked all
  thirty-six files. Once the pull request is merged the default branch's
  README will show that address before it answers. It closes with T-102.
- [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) — the fonts carry
  no licence text of their own and an embedding field that says "preview
  and print". Both are set where the fonts are built; backlog task T-101
  takes in a build that sets them.
- [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) — the
  dependency updater is set to open pull requests against `dev`. Each must
  be searched and read before it is merged (T-013's clause); none has
  arrived yet, and its one run so far ended in failure.
- [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) — the
  completed-tasks ledger's entry for T-002 lists `Cargo.lock` among the
  files modified, and that commit does not change it. The ledger is
  append-only, so the line stands and is corrected here.
- [INT-0005](../../../intents/INT-0005-versioned-releases.md) — CI names
  Ubuntu 24.04 because the pinned browser driver does not run on the
  newest. The two must be moved together when either is.

## Coverage Observations
- Every EARS clause of the build plan has at least one named test, and
  all have run but one: T-013's third clause, whose test
  `review_pull_request_text` the Loop phase makes before the pull request
  is opened. Every affected acceptance criterion is in the table above.
  Eighty-five distinct automated tests ran, 123 cases in all.
- The whole suite runs on two systems, Windows and Linux, and with the
  oldest Node the README promises (20, in CI) and a newer one (24.12.0,
  here).
- What rests on a reading and not on a test: the README's checklist (one
  paragraph of it is now held by a test), and the own-terms review, which
  cannot be a check inside the repository without holding the names it
  forbids.
- A judgement made in reading the README, owned here: the plan allows the
  README to say of the look "its name and that it is to come". The README
  still says the kit's page is "set in Cruor", and names the look's
  colours, stylesheet and theme file as "what is built next". The first is
  read as saying which typeface the kit holds, which is in the kit today;
  the second as part of saying that the look is to come. The critic read
  it the same way. The new test holds only the paragraph that first names
  the look, so the rest of this item stays a reading at each sprint.
- INT-0001 criterion 1 says the public repository holds the Book and the
  README. GitHub reports the repository as public, with `main` as its
  default branch, and `main` still holds the project's first commit alone:
  the README and everything else are on `dev`. The criterion becomes true
  of the default branch when this sprint's pull request is merged, which
  is the owner's to do.
- The same is true of INT-0002. Its criteria also speak of what "the
  repository holds", its six criteria are proven on `dev`, and the fonts
  reach the default branch with the same merge. This report holds both
  intents to the same measure: an intent whose criteria speak of the
  repository is not `realized` on the work branch's evidence alone, so
  INT-0002's move to `realized` waits for the merge too.
- CI keeps each bundle for thirty days. After that the two SHA-256 values
  recorded in the integration record are what remains of the comparison
  between systems.
- The specimen's sentence uses only characters every one of the thirty-two
  fonts holds, so a face that reports as loaded is the face that draws the
  line. The critic checked this against the fonts' character maps.

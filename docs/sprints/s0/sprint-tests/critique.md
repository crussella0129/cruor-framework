# Test Critique — Sprint 0

The third and last critique of the Test phase's evidence, as the critic
wrote it, with a **Response** added beneath each concern. It was made of
the records at `49dd8934f7f04f721504e7cbd0ef2c1d45209ccf` and of the draft
of the test report. Its four concerns are all about the report's wording;
each was answered by the wording the critic gave, and the report committed
beside this file is the draft so changed. No test, code or record of
results changed after this reading, but for one comma in the integration
record. The earlier critiques are [critique-round-1.md](critique-round-1.md)
and [critique-round-2.md](critique-round-2.md).

Third reading, of the records remade at tested commit `49dd8934f7f04f721504e7cbd0ef2c1d45209ccf`, the tests changed in `c2c6a8b`, entry 6 of the review, the Responses in `critique-round-2.md`, and the draft of the test report. Read-only: nothing in the repository or the draft was changed, and neither the test suite nor cargo was run. Checks I made myself are marked "checked".

All three second-round concerns are settled, and the tests and the three records now stand without a concern. What is left is in the draft report alone: four places where its wording says a little more, or a little less, than the evidence. None needs a test, a commit to the code or another CI run; each can be closed by the wording given.

## Concerns

### C-001: The report says every EARS clause has a test that ran, and one has not
- **Where:** draft `test-report.md`, "Coverage Observations", first item; `build-plan.md` T-013 third clause; `integration-tests.md` table of the reviews
- **Quote:** "Every EARS clause of the build plan has at least one named test that ran"
- **Failure mode:** EARS-coverage
- **Why it matters:** T-013's third clause ("WHEN a pull request, a tag or a release is about to be made…") has one named test, `review_pull_request_text`, and the report's own Summary gives it as "not yet due". The sentence is true of every other clause (checked against the plan's table), so it overstates by exactly one.
- **Suggested response:** tighten-assertion, in the wording: "Every EARS clause of the build plan has at least one named test, and all have run but one: T-013's third clause, whose test `review_pull_request_text` the Loop phase makes before the pull request is opened."
- **Response:** tighten-assertion in the wording, done. The report's first item under "Coverage Observations" now says so in the words given.

### C-002: The report passes the README's checklist without saying its own example cannot run yet
- **Where:** draft `test-report.md`, the row for INT-0005 criterion 6, the Summary's "8 passed", and "Technical Debt Identified"; `integration-tests.md` "The commands"
- **Quote:** "met, but for the one below that cannot be yet" (the integration record); the report's row says only "pass"
- **Failure mode:** evidence-drift
- **Why it matters:** The checklist's first item is that every command the README shows "was run as written and did what the README says". The fetch command as the README writes it exits 1 with HTTP 404, because `v0.1.0` does not exist. The record says so and shows the same command working against the bundle served locally. The report counts `review_readme_against_checklist` among its eight passes and nowhere carries that qualifier. Once the pull request is merged, the default branch's README will show an address that answers 404 until the owner has the tag pushed.
- **Suggested response:** defer-with-rationale, written into the report. Add to "Technical Debt Identified" under INT-0005: "the README's worked example names the address of `v0.1.0`, which answers HTTP 404 until that release exists. The command as written was run and failed as the example says it does; given the same bundle served on this machine it fetched and checked all thirty-six files. It closes with T-102." And let the criterion 6 row say "pass; the example's own address does not answer yet (see Technical Debt)".
- **Response:** defer-with-rationale, written into the report in three places: the row for INT-0005 criterion 6, the Summary's line on the integration tests, and a new item under "Technical Debt Identified", which also says that the default branch's README will show the address before it answers. It closes with T-102, when the owner has the tag pushed.

### C-003: INT-0002 is called proven and eligible while the default branch holds no font
- **Where:** draft `test-report.md`, the row for INT-0002 criterion 6 and the item on INT-0001 criterion 1 under "Coverage Observations"; INT-0002 criteria 1, 2 and 6
- **Quote:** "All six criteria are proven; the intent is eligible for `realized` once its completion evidence is attached at the Loop phase"
- **Failure mode:** intent-coverage
- **Why it matters:** The report rightly marks INT-0001 criterion 1 "not yet true of the default branch". INT-0002's criteria are worded the same way ("The repository holds the thirty-two `.woff2` files…"), and `main` is still the first commit alone (checked: `7832759`). The report holds one intent to the default branch and the other to `dev` without saying why. The Loop phase comes before the merge, so INT-0002 could be marked `realized` while what a visitor sees by default has no fonts in it.
- **Suggested response:** defer-with-rationale, in the wording. Add to the item on criterion 1 under "Coverage Observations": "The same is true of INT-0002: its six criteria are proven on `dev`, and the fonts reach the default branch with the same merge." Then say which the Book means: that an intent is realized on the work branch's evidence, or that INT-0002's move to `realized` also waits for the merge. Either is defensible; the report should choose.
- **Response:** defer-with-rationale, and the report chooses: an intent whose criteria speak of what the repository holds is not `realized` on the work branch's evidence alone. INT-0002's six criteria are proven on `dev`, and its move to `realized` waits for the merge that brings the fonts to the default branch. The row and a new item under "Coverage Observations" say so, and the intent's own history records it.

### C-004: Three small slips of naming and count in the draft and one record
- **Where:** draft `test-report.md`, the rows for INT-0002 criterion 5 and INT-0005 criterion 5, and "Failures" item 3; `integration-tests.md` "The repository as it stands"
- **Quote:** "the nine `manifest_*` and `check_*` tests"
- **Failure mode:** evidence-drift
- **Why it matters:** Each is trivial alone, but the report is the page the intents will link to as their evidence.
  - `tests/manifest.rs` holds nine tests, of which eight bear those names (seven `manifest_*` and `check_runs_both`); the ninth is `repository_passes_check`.
  - The plan traces `test_crate_version_is_first_release` to INT-0005 criterion 5 ("the first tag is the crate's version"), and the row for that criterion leaves it out.
  - In the integration record, "found at `6c9fb0b` (CI run 45246763880) at `3b7b3d3` and at `acee815`" lacks a comma after the bracket, and reads as if that run were at `3b7b3d3`.
- **Suggested response:** tighten-assertion, in the wording: "the nine tests of `tests/manifest.rs`"; add `test_crate_version_is_first_release` (T-001) to the criterion 5 row; add the comma. In "Failures" item 3, "the critic twice searched" may now read "at each of its three readings" (see below).
- **Response:** tighten-assertion in the wording, all four done as given: the nine tests are named by their file, the row for INT-0005 criterion 5 names `test_crate_version_is_first_release` and T-001, the comma is in the integration record, and "Failures" item 3 says the critic searched at each of its three readings.

### Looked at and not raised

Settled from the second round:

- **Round-2 C-001 (Responses citing an empty report): settled.** The draft exists and holds all four things: the deviation under "Failures" item 3 and in the row for INT-0001 criterion 5; the judgement on the look under "Coverage Observations"; criterion 1 in its row and under "Coverage Observations"; the T-002 ledger line under "Technical Debt Identified". INT-0005 criterion 5 is "not yet proven" and the intent is held short of `realized`. The three reworded Responses in `critique-round-1.md` name those sections correctly.
- **Round-2 C-002 (two sentences): settled.** The integration record now says which entry speaks for which commits, and that the new test holds one paragraph while the rest of the item stays a reading.
- **Round-2 C-003 (commands matched by a fragment): settled.** `test_release_workflow_runs_guards_then_bundle_then_publish` asserts both `run` values of `release.yml` whole. `test_ci_workflow_runs_guards` asserts one guards step, the command whole, no condition on it, and no `continue-on-error` on any job or step of `ci.yml`. Both agree with the workflows as they stand (checked by reading).

Checked this round:

- **Tested commit and CI run.** `origin/dev` is `49dd893`. Run 45266754572 is a push run on `dev` at that commit, concluded `success`, every step green; its log shows `cargo test` as 7 + 11 + 1 + 4 + 9 = 32 passed and `pytest` as "91 passed". Its artefact `cruor-framework-bundle` exists and has not expired. CI was `success` at all four commits the report names (`6c9fb0b`, `3b7b3d3`, `acee815`, `49dd893`).
- **The report's counts.** All agree with the test files and the records:
  - 74 unit tests (63 planned, 11 beyond the plan);
  - 11 integration tests, as 8 passed, 2 met with the deviation and 1 not yet due;
  - 10 end-to-end tests (9 planned, 1 beyond);
  - 73 automated tests the plan names (63 unit, `repository_passes_check`, 9 end-to-end);
  - 85 distinct tests (32 in Rust, 53 in Python) and 123 cases (32 + 91).
- **The remade records.** Nothing went stale in the remaking:
  - eight pushes, the last six each with an entry made first; entry 6's commit (16:09:20) precedes its push (16:09:25);
  - 39 commits, as 28 in ranges, 5 that only add an entry and 6 covered after the fact;
  - four commits that belong to no task (`446ceb5`, `27fc856`, `3ab351a`, `c2c6a8b`);
  - five planned tests listed as tightened; the earlier runs' ids are right.
- **What the two commits change.** `c2c6a8b` changes `tests/test_ci.py` and `tests/test_release.py` alone; `49dd893` changes the review record alone. The locked plans are untouched, and nothing a release holds has changed since `3b7b3d3`, so the `manifest.json` hash I rebuilt in round 1 still stands.
- **The rest of the Intent Verification table.** Every other row is fair to its criterion. INT-0005 criterion 5 is stated as unproven, with what it rests on. INT-0001 criterion 5 is "met, with a deviation", not a pass. Criteria 2 and 4 of INT-0001 are said to wait for the look.
- **"Failures" and "Technical Debt Identified".** Each item agrees with the records. The updater has run once, at `165d4a1`, and failed; GitHub still lists no pull request, no release and no tag; the repository is public with default branch `main`.
- **What the report says of the critic.** It is accurate: I read the look's judgement the same way, I checked the specimen's sentence against the fonts' character maps, and I searched the history with a list of my own. That search has now been made at each of the three readings, the last over all 39 commits, their messages, the remade records, both earlier critique files and the draft; it finds none.
- **`critique-round-2.md`.** It gives my second critique as I wrote it.

## Confidence
proceed-with-caveats

# Test Critique — Sprint 0, round 2

The second critique of the Test phase's evidence, as the critic wrote it,
with a **Response** added beneath each concern. It was made of the records
at `acee815beae9dacdfd6d8e72ea318b29ae08d2a5`. The tests it asked for were
tightened in `c2c6a8bfa75bc8e1fe4ab90b0f85fb606ebf20da`, the records were
made again at the commit after it, and the critic read them a third time:
that reading is [critique.md](critique.md). The first critique is
[critique-round-1.md](critique-round-1.md).

Second reading, of the records remade at tested commit `acee815beae9dacdfd6d8e72ea318b29ae08d2a5`, the tests changed in `3ab351a`, entry 5 of the review, and the Responses in `critique-round-1.md`. Read-only: nothing in the repository was changed, and neither the test suite nor cargo was run. Checks I made myself are marked "checked".

All eight first-round concerns are answered in substance. Three small ones stand: one is about what the Responses promise of a report not yet written, one is two sentences that say slightly more than the evidence, and one is new.

## Concerns

### C-001: Three Responses say what the test report holds, and the report is empty
- **Where:** `critique-round-1.md` Responses to C-002, C-004 and C-008; `integration-tests.md` `review_commits_touch_only_their_tasks`; `docs/sprints/s0/sprint-tests/test-report.md`
- **Quote:** "the test report carries it as a deviation, not a plain pass"
- **Failure mode:** evidence-drift
- **Why it matters:** `test-report.md` is 0 bytes at the tested commit and in the working tree. The Responses are written in the present tense about a file that will be written after this reading, and no critic reads it afterwards. Four things are promised to it:
  - the deviation for three pushes (C-004);
  - the judgement on what the README says of the look (C-002);
  - INT-0001 criterion 1 as "proven on `dev` and not yet true of the default branch" (C-008);
  - the T-002 ledger line that wrongly lists `Cargo.lock`.
- **Suggested response:** defer-with-rationale. Write the report so that each of the four is in it, and leave INT-0005 short of `realized`, since criterion 5 waits for T-102. Reword the three Responses to say the report "will" carry these, or add the report's section names once it exists.
- **Response:** accepted. The phase's order is that the report is written only once the last critique allows it, so it could not exist at this reading. To close the gap the report was drafted before the third reading and the critic was given the draft to read with the records; the report committed is that draft. The three Responses of the first round now name the report's sections. The four things are in it: the deviation under "Failures" and in the row for INT-0001 criterion 5; the judgement on the look under "Coverage Observations"; criterion 1 in its row and under "Coverage Observations"; the ledger line under "Technical Debt Identified". INT-0005 is left short of `realized`.

### C-002: Two sentences in the integration record say slightly more than the evidence
- **Where:** `integration-tests.md` "The deviation" and "What is said of the look"
- **Quote:** "entry 2 only says so afterwards" and "so the words taken out cannot come back unnoticed"
- **Failure mode:** evidence-drift
- **Why it matters:** Both are small, but these are the two paragraphs rewritten to be exact.
  - Entry 2 says "searched before the first push" only of `03ad441` and `7c97e55`. For the four Research and Plan commits it is entry 1 that says so ("The commits before them were searched before they were pushed"). So two entries say it afterwards, each for its own commits.
  - `test_readme_says_of_the_look_only_its_name` holds one paragraph, the second of the README. A description of the look added to any other paragraph would pass it. Its name and the record's sentence promise the whole README, and the rest of the checklist item is still a reading.
- **Suggested response:** tighten-assertion, in the wording only: "entries 1 and 2 only say so afterwards", and "cannot come back to that paragraph unnoticed; the rest of the README stays a reading at each sprint". No test change is needed.
- **Response:** tighten-assertion in the wording, done. Both sentences of the integration record now say what the critic gives: which entry speaks for which commits, and that the test holds one paragraph while the rest of the item stays a reading at each sprint.

### C-003: The workflow tests find the guards and the bundle by a fragment of the command
- **Where:** `tests/test_release.py` `index_of`, `test_release_workflow_runs_guards_then_bundle_then_publish` and `test_release_workflow_has_no_continue_on_error`; `tests/test_ci.py`; `build-plan.md` T-010 second clause and T-001 third clause
- **Quote:** `guards = index_of(steps, "bash tools/run-guards.sh")`
- **Failure mode:** weak-assertion
- **Why it matters:** New this round; I passed over it in the first. In `release.yml` the gate step and the "make public" step are asserted whole, but the guards and bundle steps are matched by substring. `bash tools/run-guards.sh || true` would pass every test and publish with failing guards. For `ci.yml` the command is matched whole, but no test forbids `continue-on-error` on its steps, so "CI SHALL … fail if it fails" is held only by the file as it stands. Both workflows are right today. These text tests are all that criterion 5 rests on until T-102.
- **Suggested response:** tighten-assertion: assert the two `run` values of `release.yml` whole (`bash tools/run-guards.sh`, and `cargo run --release -- bundle --out dist --tag "$TAG"`), and run the no-`continue-on-error` loop over `ci.yml` too. Otherwise defer-with-rationale; this is small enough to carry as a caveat without another round.
- **Response:** tighten-assertion, done, and not carried as a caveat, since these tests are what criterion 5 rests on for now. `test_release_workflow_runs_guards_then_bundle_then_publish` asserts both `run` values whole. `test_ci_workflow_runs_guards` asserts that the guards are one step with the command whole and no condition, and that no job or step of `ci.yml` is told to carry on after an error. Both pass against the workflows unchanged.

### Looked at and not raised

Settled from the first round:

- **Round-1 C-001 (family never made to disagree): settled.** `test_check_fonts_fails_on_fonts_swapped_across_families` swaps two Regulars across families and asserts a `family:` line for each file with what the font says of itself, and that nothing but family is at fault. `test_check_fonts_fails_on_wrong_family_in_rule` asserts the exact line naming file, field and both values. Both comparisons in `tools/check_fonts.py` now run on a failing path.
- **Round-1 C-002 (the README fault held by no test): settled, but for the wording above.** The pinned paragraph is the README's as it stands (checked). The judgement is now made in the open and I find it fair: "set in Cruor" names what the kit holds today, and the three parts are named only as what is built next.
- **Round-1 C-003 (the stand-in answers anything): settled.** The stand-in records its arguments, and two tests assert the whole call, once, across an empty, a public and a draft answer. The pinned expression is the script's own text; that it yields tag, tab, `false` on real data rests on my read in round 1. The Response is honest that a real draft's row stays unobserved until T-102.
- **Round-1 C-004 (pushes ahead of their entry): settled, but for the wording above.** The table's result is now a stated deviation for three pushes, and entry 5 carries the note on entry 1.
  - Checked: `origin/dev` has been pushed seven times, and entry 5's commit (16:01:08) precedes its push (16:01:14).
  - Checked: 37 commits, as 27 in ranges, 4 that only add an entry, and 6 covered after the fact.
  - Checked: my own search, now run over all 37 commits, their messages, the three remade records and `critique-round-1.md`, still finds none.
- **Round-1 C-005 (the redirect): settled.** `test_fetch_release_follows_a_redirect` gives the example only the redirecting address, and asserts exit 0, 37 files identical to the bundle's, and that the address behind was asked for exactly those 37. No timing or shared state. The e2e record fairly says what is left for the real run.
- **Round-1 C-006 (carriage returns): settled.** The test now requires exit 1.
- **Round-1 C-007 (the licence's body): settled.** The pinned SHA-256 is that of `fonts/OFL.txt` from its second line (checked: `3e30b6b3…861f`, in the working tree and in git, with no carriage return). I read the body and it is the licence as I know it. That it matches the published text byte for byte still rests on entry 1's comparison.
- **Round-1 C-008 (criterion 1 on the default branch): deferred with a sound rationale,** subject to C-001 above. `origin/main` is still `7832759`.

Checked afresh this round:

- **Tested commit and CI run.** Run 45265330443 is a push run on `dev` at `acee815`, concluded `success`, every step green. Its log shows `cargo test` as 7 + 11 + 1 + 4 + 9 = 32 passed and `pytest` as "91 passed". Its artefact `cruor-framework-bundle` exists and has not expired.
- **Counts.** 91 is the earlier 86 plus the five new tests. Planned unit tests are 63, beyond the plan 11 (seven earlier, four new), planned end-to-end 9, beyond the plan 1. All agree with the test files.
- **What the two commits change.** `3ab351a` changes seven files under `tests/` and nothing they exercise. `acee815` changes the review record alone. The locked plans are untouched.
- **`ci_bundle_matches_local`.** Nothing a release holds changed since `3b7b3d3`, so the `manifest.json` hash I rebuilt in round 1 (`6fe8d4b2…2ff6`) still stands. The archive's hash I could not rebuild.
- **`review_updater_pull_requests`.** GitHub still lists no pull request, no release and no tag.
- **`critique-round-1.md`.** It gives my first critique as I wrote it.
- **The new tests.** None is flaky or depends on order. Only the gate's pinned call mirrors its implementation, which is what holding a call means.

## Confidence
proceed-with-caveats

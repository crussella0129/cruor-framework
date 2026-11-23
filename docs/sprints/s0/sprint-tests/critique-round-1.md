# Test Critique — Sprint 0, round 1

The first critique of the Test phase's evidence, as the critic wrote it,
with a **Response** added beneath each concern. It was made of the records
at `3b7b3d34de3f6ef75b61a912a06b6ce67525c917`. The tests it asked for were
written in `3ab351acdc88b786eabaa22e68ccc54cbdfe0b62`, the records were made
again at the commit after it, and the critic then read them a second time
([critique-round-2.md](critique-round-2.md)) and a third
([critique.md](critique.md)). Three Responses below speak of the test
report; after the second critique they were reworded to say where in the
report each thing is.

Read-only review of the records at tested commit `3b7b3d34de3f6ef75b61a912a06b6ce67525c917`. Nothing in the repository was changed, and neither the test suite nor cargo was run. Checks I made myself are marked "checked".

## Concerns

### C-001: No test makes a font disagree about its family
- **Where:** `tests/test_check_fonts.py` `test_check_fonts_fails_on_swapped_fonts` and `test_check_fonts_fails_on_wrong_weight_in_rule`; `build-plan.md` T-006 second clause; INT-0002 criterion 5
- **Quote:** "WHEN any font disagrees with its family or its rule, THEN it SHALL exit non-zero and name the file and the field that disagrees." The swap test ends with "# No other family is named."
- **Failure mode:** negative-path
- **Why it matters:** Criterion 5 names "a font's own name for its family and style". Both negative tests stay inside one family (a Bold and an Italic of Cruor Lite Regular change places; one rule's weight is changed). The two `family:` comparisons in `tools/check_fonts.py` therefore run only on the passing path, and nothing shows that a font filed under another family's stem, or a rule with the wrong `font-family`, is refused and named.
- **Suggested response:** add-test. Swap two fonts of the same style across families (say `CruorSansMono-Regular.woff2` and `CruorLiteMono-Regular.woff2`) and assert a line beginning `<file>: family:`. A second case could change one rule's `font-family` in a copy of `fonts.css`.
- **Response:** add-test, done. `test_check_fonts_fails_on_fonts_swapped_across_families` swaps those two fonts and asserts that each file is named with `family:` and what the font says of itself; `test_check_fonts_fails_on_wrong_family_in_rule` changes one rule's `font-family` and asserts the line that names the file, the field and both values. Both pass, so both comparisons refuse what they should.

### C-002: The one fault the Test phase found is held by no test
- **Where:** `integration-tests.md` "What is said of the look"; `tests/test_readme.py` `test_readme_says_what_the_kit_is`; commit `27fc856`
- **Quote:** `assert "gives a web page the look called **Cruentous Atonement**" in FLOWED`
- **Failure mode:** weak-assertion
- **Why it matters:** That assertion held at `6c9fb0b`, where the README went on to describe the look, and holds at `3b7b3d3`. Commit `27fc856` changes `README.md` alone, so a later edit could put a description back and all 86 Python tests would still pass. The "met" verdict at `3b7b3d3` also rests on a reading: the README still says the look is "set in Cruor" and lists "its colours, its stylesheet and its theme file". The record discloses both, and whether they sit inside "its name and that it is to come" is a judgement the report should own.
- **Suggested response:** add-test, pinning the paragraph that first names the look to `A kit that gives a web page the look called **Cruentous Atonement**, set in Cruor.` Otherwise defer-with-rationale, saying this item stays a reading at each sprint.
- **Response:** add-test, done. `test_readme_says_of_the_look_only_its_name` holds that paragraph whole; the sprint that builds the look changes the test with the README. The judgement is made in the integration record, under "What is said of the look", and again in the test report under "Coverage Observations": "set in Cruor" says which typeface the kit holds, which is in the kit today, and the three parts named are named only as what is built next.

### C-003: The stand-in for the GitHub client answers whatever it is asked
- **Where:** `tests/test_release.py` `STAND_IN_GH` and the four `test_release_gate_*` tests; `tools/release-gate.sh`
- **Quote:** `printf '%s' "$STAND_IN_RELEASES"`
- **Failure mode:** stub-leak
- **Why it matters:** The stand-in ignores its arguments and returns rows already in the shape the script's own `--jq` expression is meant to produce. A wrong API path, a dropped `--paginate` or a wrong expression would pass all four tests. The unsafe direction is a row that never matches, which lets the gate pass over a leftover draft.
- **Checked:** I ran the gate's listing for real, read-only. Against this repository it exits 0 with no rows. Against a public repository that has releases, the rows come back as tag, tab, `false`. The call and the row shape are right today; a draft's row (`true`) could not be observed.
- **Suggested response:** tighten-assertion. Have the stand-in record its arguments and assert the call (`api --paginate repos/{owner}/{repo}/releases --jq …`). Otherwise defer-with-rationale, citing the real read above and T-102.
- **Response:** tighten-assertion, done. The stand-in now notes every argument it is given. `test_release_gate_passes_on_main` and the new `test_release_gate_asks_for_every_release` assert the whole question: `api`, `--paginate`, the path, `--jq` and the expression, asked once, whatever the answer. What stays unobserved is a draft's row as GitHub itself gives it; the first real release is where a draft first exists (T-102).

### C-004: "Passed, with the remark" understates how many pushes went out ahead of their entry
- **Where:** `integration-tests.md` `review_own_terms_before_each_push`, the table and the Remark; `own-terms-review.md` entries 1, 2 and 4
- **Quote:** "For those pushes the clause "an entry, made before it" is met after the fact, by entry 4, and not before."
- **Failure mode:** evidence-drift
- **Why it matters:** The Remark names the Research and Plan pushes only. The record's own count shows a third: the first Build push (head `7c97e55`) carried `03ad441` and `7c97e55`, which entry 1's range does not hold. `03ad441` also changes the two ledgers, so it is not "a commit whose only change is a new entry". The claim that all of these were "searched at the time" has no artefact. The test plan's wording for this test asks for an entry made before every push.
- **Checked:** The remote branch's push history shows six pushes, at `165d4a1`, `6f2c638`, `7c97e55`, `db6fad0`, `6c9fb0b` and `3b7b3d3`. Each entry's commit predates its push, and every entry's file list agrees with git for all 35 commits. I searched every tracked text file at every commit, and every commit message, against a list of my own of over a hundred names, and read every name-table string of the 32 fonts. I found none, and no font has a metadata or private block.
- **Suggested response:** defer-with-rationale. Carry it into `test-report.md` as a stated deviation ("met after the fact for three pushes"), not a plain pass, and have the Remark name the first Build push or say why ledger lines needed no entry.
- **Response:** accepted as written. The integration record now says the clause was met after the fact for three pushes and names the first Build push; the review's own record says so too, in a note on entry 1 within entry 5; and the test report, written once the last critique allowed it, carries it under "Failures" as a deviation, not a plain pass. The critic's own search of the whole history with another list is a second reading that found none.

### C-005: The redirect is left to the first real release, though it can be met locally
- **Where:** `e2e-tests.md` "Not yet possible"; `build-plan.md` T-009 Notes; `tests/test_fetch_release.py`
- **Quote:** "What no local test meets is the redirect a real release's address answers with; that run is where it is first exercised."
- **Failure mode:** e2e-cop-out
- **Why it matters:** `release_checks_itself_v0_1_0` is fairly marked not yet possible and its unlock is credible: T-102 is in `docs/work/tasks.md` and waits on the owner's word. One part of it is possible now. A local server that answers each file with a 302 to a second local address would exercise redirect-following deterministically, instead of on the one run that makes a release public and then has to withdraw it.
- **Suggested response:** add-test (`test_fetch_release_follows_a_redirect`, two local servers). Otherwise defer-with-rationale, citing the withdrawal step as the mitigation the plan chose.
- **Response:** add-test, done. `test_fetch_release_follows_a_redirect` runs the example against a second local address that answers every request with a 302 to the first, and asserts that all thirty-seven files arrive identical to the bundle's and that each was asked of the address behind the redirect.

### C-006: The carriage-return test passes if git fails
- **Where:** `tests/test_repository.py` `test_tracked_text_has_no_carriage_returns`
- **Quote:** `check=False,` then `assert found.stdout.splitlines() == []`
- **Failure mode:** weak-assertion
- **Why it matters:** `git grep` exits 1 for "none found" and 128 for an error, and both give empty output. The test tells a clean repository from a search that never ran only by luck.
- **Checked:** The search does find a carriage return in a scratch repository of my own (exit 0, file listed), and it exits 1 here. Today's pass is a true one.
- **Suggested response:** tighten-assertion: `assert found.returncode == 1`.
- **Response:** tighten-assertion, done as suggested.

### C-007: The licence's body is not held, only its headings
- **Where:** `tests/test_fonts_intake.py` `test_ofl_text_and_copyright_line`; `build-plan.md` T-003 second clause; INT-0002 criterion 2
- **Quote:** `assert f"\n{number}) " in conditions`
- **Failure mode:** weak-assertion
- **Why it matters:** The clause says the file "SHALL hold the text of the SIL Open Font License, Version 1.1". The test checks the first line, the version heading and that five numbered items exist, so an altered or shortened condition would pass. `bundle` would then copy it into a release under a matching checksum. This file is the only statement of the fonts' terms, and `LICENSE-APACHE` is already pinned by SHA-256 in `tests/test_licences.py`.
- **Suggested response:** tighten-assertion. Pin the SHA-256 of everything after the copyright line; entry 1 of the review already compared that text with the published one. Otherwise defer-with-rationale.
- **Response:** tighten-assertion, done. The test now holds the SHA-256 of the file from its second line to its end, the text that entry 1 of the review set against the published licence.

### C-008: INT-0001 criterion 1 is true of `dev`, not yet of the repository's default branch
- **Where:** INT-0001 Acceptance criteria 1; `test-plan.md` Intent Traceability (the rows for criterion 1 are all README tests)
- **Quote:** "The public repository `crussella0129/cruor-framework` holds this Project Book and a README"
- **Failure mode:** intent-coverage
- **Why it matters:** No clause or named check covers "public" or "holds this Project Book". The README and the code are on `dev` only.
- **Checked:** GitHub reports the repository as public with default branch `main`, and `origin/main` is still the first commit (`7832759`).
- **Suggested response:** defer-with-rationale. Record the visibility in the report as observed, and leave criterion 1 to be closed at the Loop phase once the pull request is merged.
- **Response:** defer-with-rationale. The test report, in its row for the criterion and under "Coverage Observations", records what was observed (public; default branch `main`, which holds the first commit alone) and marks criterion 1 as proven on `dev` and not yet true of the default branch. It closes when the sprint's pull request is merged, which is the owner's to do. INT-0001 stays `active` in any case, since two of its criteria wait for the look.

### Looked at and not raised

- **Tested commit and CI run.** `origin/dev` is `3b7b3d3`. Run 45262447194 is a push run on `dev` at that commit, concluded `success`, with every step green. Its log shows `cargo test` as 7 + 11 + 1 + 4 + 9 = 32 passed and `pytest` as "86 passed", the totals the records give. Run 45246763880 is at `6c9fb0b`, also `success`.
- **`ci_bundle_matches_local`.** I rebuilt `manifest.json` from the tracked files without the tool; its SHA-256 is `6fe8d4b22f83d1a2491b30683cb10a8f196ed58546de01aaf3ce2c4298472ff6`, the value recorded. The archive's hash I could not rebuild. The artefact is kept for 30 days, so the recorded hashes are what will remain.
- **Counts.** 63 planned unit tests, 7 beyond the plan and 9 end-to-end tests agree with the test files; every EARS clause has a named test that exists.
- **"Sets text in it" for all 32 faces.** I suspected this rested on "loaded" for 31 of them, since the fallback test covers one family. Every character of the specimen's sentence is in every font's character map, so a loaded face is the face drawn.
- **`review_intake_matches_inventory`.** Glyph counts (328 and 779), the eight family names, weights and italic flags read from the fonts agree with the record and `font-inventory.md`; `fonts/manifest.toml` records `777120960fd302eb565806badf18a87b49beeffb`.
- **`review_updater_pull_requests`.** It passes on an empty set, and truly: GitHub lists no pull request, open or closed.
- **`review_pull_request_text` and the closing pushes.** "Not yet due" is as the locked plan has it, with the Loop phase as the unlock.
- **INT-0005 criterion 5.** The records do not claim it. It rests on tests that read `release.yml` as text until T-102, so the report should leave the intent short of `realized`.
- **Stub leakage in the guard tests.** None: the stand-ins replace only the tools, and the exact call sequence is asserted.

## Confidence
proceed-with-caveats

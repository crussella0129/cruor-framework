# Plan Critique — Sprint 0

Second review, of the plans, intents and backlog as revised after round 1. Of the nineteen round-1 concerns, the responses recorded in `critique-round-1.md` match what the plans and intents now say, with the exceptions raised below (C-002 for round-1 C-013, C-005 for round-1 C-005 and C-014). Every EARS clause now has a named test; one test has no clause (C-002).

The critic's text is given as it was returned. The line marked **Response** beneath each concern is the planner's, and says what was done.

## Concerns

### C-001: The review record cannot cover the commits that carry it, nor the pushes made after the Test phase
- **Where:** `test-plan.md` "The reviews of T-013", `review_own_terms_before_each_push` and `review_record_is_complete`; `build-plan.md` T-013 fourth clause and Notes
- **Quote:** "Pass: every commit on `dev` falls in some entry's range, and every entry's number found is none."
- **Failure mode:** hidden-dep
- **Why it matters:** Each entry lives in a tracked file, so recording a review makes a new commit that lies after "the last commit covered" and must itself be pushed; read literally, the pass condition can never hold for the newest commit and every push needs an entry that needs a push. The sprint's last pushes also fall after the Test phase reads the record: the commits that close the sprint, and the push the checkpoint helper makes itself when it opens the pull request, so `review_record_is_complete` ("no push of the sprint lacks an entry") is judged before those pushes exist. T-013 is also last in the Execution Sequence while its Notes call it "complete when the review that covers T-003's commit is recorded", which leaves open whether anything may be pushed before the Build phase reaches it.
- **Suggested response:** fix-in-plan. State that a commit whose only change is a new entry is covered by that entry; say where the reviews before the closing and checkpoint pushes are recorded and that they are outside what the Test phase judges (or have the Loop phase add and check them); and either place T-013 directly after T-003 in the sequence or say that no push is made before it.
- **Response:** fixed in plan. A commit whose only change is a new entry is covered by that entry (T-013's Notes and both tests). The reviews before the closing and checkpoint pushes go in the same file and are read at the Loop phase, before the pull request is opened; the Test phase judges the record as it stands then. T-013 now follows T-003 in the Execution Sequence, and the plan says that no Build commit is pushed before its first review.

### C-002: `review_intake_matches_inventory` asserts things no clause requires
- **Where:** `test-plan.md` Intent Traceability (the row "6, for files of any kind") and "The reviews of T-013"; `build-plan.md` T-013 sixth clause, T-003 Notes
- **Quote:** "the entry covering T-003's commit gives the full commit id of Cruor that was built, says the build's tree had nothing uncommitted, and sets the thirty-two files' glyph counts and family names against `font-inventory.md`, recording every difference."
- **Failure mode:** plan-test-mismatch
- **Why it matters:** The table traces this test to T-013's clause on listing each commit's files, which says nothing of a commit id, a clean tree or the inventory; the clean tree appears only in T-003's Notes. It is the whole answer to round-1 C-013, and a test without a clause is a promise the Build phase is not bound to keep.
- **Suggested response:** fix-in-plan. Add a clause to T-003 or T-013: "WHEN the review covers the commit that takes the fonts in, THEN its entry SHALL give the full commit id built, state that the tree had nothing uncommitted, and set the fonts' glyph counts and family names against `font-inventory.md`", and trace the test to it.
- **Response:** fixed in plan. T-013 has that clause, and the test traces to it in a row of its own.

### C-003: Nothing says what follows when the release's own check fails, or when a draft is left behind
- **Where:** `build-plan.md` T-010 third and fourth clauses and Notes; INT-0005 criterion 5
- **Quote:** "WHEN the release is public, THEN `release.yml` SHALL run `examples/fetch-release.mjs` against the release's own address, pinned to the SHA-256 of the manifest it built, and SHALL fail if that does not exit 0."
- **Failure mode:** missing-risk
- **Why it matters:** By then the release is public and, by the second clause, can never be published again for that tag. The Notes concede that this step is the first time the example meets a real release address and its redirect, so the likeliest first failure is in the check itself, on the one run that cannot be repeated. A run that stops between creating the draft and making it public likewise leaves a draft that makes every re-run fail as "a release for the tag already exists".
- **Suggested response:** fix-in-plan. Add clauses for both states: on a failed self-check the workflow SHALL return the release to a draft (or leave it and stop for the owner; choose one and say so), and a leftover draft for the tag SHALL be named in the failure so the owner can remove it. Record the chosen recovery in T-102.
- **Response:** fixed in plan. On a failed check the workflow returns the release to a draft before it fails, so nothing stays public that has not proven itself; the gate names a leftover draft for the owner to remove; the workflow never deletes a release. T-102 records what was done if a run leaves a draft. Tests: `test_release_workflow_withdraws_on_failed_check`, `test_release_gate_names_leftover_draft`.

### C-004: The gates that keep a wrong tag from publishing are tested only as text
- **Where:** `test-plan.md` T-010 unit tests
- **Quote:** "These read `release.yml` as data; none of them publishes anything."
- **Failure mode:** e2e-drift
- **Why it matters:** `test_release_workflow_requires_main` and `test_release_workflow_refuses_existing_release` show that a step with the right shape is present, not that it refuses; a wrong comparison or a shallow checkout would pass every test and be found only on the first real tag. The ancestry check is plain git and can be exercised now.
- **Suggested response:** fix-in-plan. Put the two gates in a script under `tools/` that the workflow calls (adding it to T-010's Touches), and test it: against a scratch repository for a tagged commit on and off `main`, and with a stand-in for the GitHub client for a release that exists. If not taken, defer-with-rationale in T-010's Notes.
- **Response:** fixed in plan. The gates are `tools/release-gate.sh`, in T-010's Touches, with a clause and four tests that run it against a scratch repository and a stand-in for the GitHub client. `test_release_workflow_calls_gate` also requires the workflow's checkout to have the whole history of `main`.

### C-005: Two decisions made in answer to round 1 are recorded only in task Notes
- **Where:** `build-plan.md` T-010 Notes and T-009 Notes; INT-0005 Rationale and Alternatives
- **Quote:** "A protected environment with a required reviewer was considered and not taken: it is a setting of the repository the owner would have to keep, and tags are pushed only on the owner's word."
- **Failure mode:** intent-drift
- **Why it matters:** That is an alternative with its reason, and it stands only in sprint prose and in `critique-round-1.md`. So does the finding in T-009's Notes that "without it the check shows only that the files and the manifest agree with each other", which qualifies INT-0005's own rationale ("a pinned version with checksums means a build gets exactly what it expects") without the intent saying that a build must pin the manifest's SHA-256 to get that.
- **Suggested response:** fix-in-plan, in the intent: add the protected environment to INT-0005's Alternatives, and say in its Intent or Rationale that the checksum a build pins is the manifest's.
- **Response:** fixed, in the intent. INT-0005's Alternatives record the protected environment and why it was not taken, and its Rationale says that the checksum a build pins is the manifest's.

### C-006: INT-0002 now states as fact what the intake will hold, and the plan lets it differ
- **Where:** INT-0002 Consequences (revised); `build-plan.md` T-003 Notes; `font-inventory.md`
- **Quote:** "Cruor's next characters are still being drawn, so the first intake holds Latin through Latin Extended-A."
- **Failure mode:** intent-drift
- **Why it matters:** T-003 takes "the head of its working branch when this task runs", and `review_intake_matches_inventory` exists to record differences from the inventory, so the stable chapter asserts a coverage that is only known once T-003 has run. It is also already narrower than the inventory, which gives the Mono and Pixelated families box drawing, block elements and more beyond Latin Extended-A.
- **Suggested response:** fix-in-plan, in the intent: drop the coverage from the sentence or word it as what the inventory of 23 November found, and let the review's entry and the manifest say what was taken in.
- **Response:** fixed, in the intent. INT-0002 no longer says in advance what the first intake covers; the manifest and the review of the intake say what was taken in.

### C-007: Pull requests the repository opens by itself cannot be read "first"
- **Where:** `build-plan.md` T-013 third clause; `.github/dependabot.yml` (already tracked)
- **Quote:** "WHEN a pull request, a tag or a release is about to be made, THEN the same search and reading SHALL be made of its title, its body and its message first."
- **Failure mode:** missing-risk
- **Why it matters:** The repository already carries an updater that opens pull requests against `dev` each week for the actions the workflows use, which T-001 and T-010 now introduce. Their titles, bodies (which quote other projects' release notes) and commit messages are written by a service, so the clause cannot be met for them, and INT-0001's boundary counts a "record here".
- **Suggested response:** fix-in-plan. Add a clause for records the owner does not write: each is read on arrival, and one that fails is closed, not merged; or switch the updater off until a sprint decides how it is kept. Say which.
- **Response:** fixed in plan. The updater stays on. T-013 has a clause for pull requests the owner did not write: each is searched and read before it is merged, and one in which something is found is closed, not merged. Test: `review_updater_pull_requests`.

### C-008: Two of the new browser tests cannot be carried out as worded
- **Where:** `test-plan.md` End-to-End Tests, `test_specimen_fetches_a_file_for_each_face` and `test_specimen_styles_of_a_family_differ`; `build-plan.md` T-007 first clause
- **Quote:** "each line's request is the file its family and style call for."
- **Failure mode:** plan-test-mismatch
- **Why it matters:** On one page load a font request belongs to a face, not to a line, so the test as written can show only that thirty-two files were fetched, not which request answered which line. The picture test compares "the four lines" of a page whose lines are "labelled": if the label is in the picture the four differ whatever font is drawn, and a browser's own imitation of bold or italic would differ too.
- **Suggested response:** fix-in-plan. For the first, ask for each face alone through the browser's font-loading interface and assert the one file fetched for it. For the second, picture the sentence without its label; the first test then carries the proof that the difference comes from the right file.
- **Response:** fixed in plan. Each face is asked for alone on a fresh page and the one file fetched is checked; the pictures are of the sample sentences without their labels, which T-007 now keeps in separate elements.

### C-009: Small gaps left by the rewrite
- **Where:** `build-plan.md` T-001 and T-013 second clause; `test-plan.md` `test_fetch_release_matches_repository`
- **Quote:** "every font, `fonts.css` and `OFL.txt` in that folder is byte-identical to the file in `fonts/`"
- **Failure mode:** plan-test-mismatch
- **Why it matters:** Three loose ends. INT-0005 criterion 4 says "files identical to the repository's", yet the two code licences the example fetches are compared with nothing in the repository. The intents and `release_checks_itself_v0_1_0` assume the crate's version is 0.1.0, but no clause or test fixes it, so a mismatch surfaces only when the tag is refused. And T-013 reads "every name-table string" of each font, while a `.woff2` can also carry a metadata block and a private block outside its tables, which that reading does not open.
- **Suggested response:** fix-in-plan. Compare `LICENSE-MIT` and `LICENSE-APACHE` with the root's files in the fetch test; add to T-001 a clause and test that the crate's version is `0.1.0`; and have T-013's second clause and `review_font_name_tables` also record that each font's metadata and private blocks were read, or are absent.
- **Response:** fixed in plan, all three. The fetch test compares the two licences with the root's files; T-001 has a clause and a test that the crate's version is `0.1.0`; T-013 and `review_font_name_tables` cover each font's metadata and private blocks.

## Confidence
proceed-with-caveats

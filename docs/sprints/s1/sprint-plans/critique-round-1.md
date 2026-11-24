# Plan Critique — Sprint 1, first round

The critic's concerns are given here as it returned them, each cut to its
label, where it stands and why it matters, and followed by what was done.
Its verdict on this round was `block`. The plans were then rewritten and
reviewed again; the last round is in `critique.md`.

## Concerns

### C-001: The foot of a carved heading cannot meet T-203's own clauses with the look's colours
- **Where:** `build-plan.md` T-203; INT-0003 criteria 3 and 4
- **Failure mode:** EARS-vague
- **Why it matters:** the foot stop `#ba1a1a` stands at about 3.11 on the flat page and about 2.80 on the stone at its brightest, so the two clauses cannot both hold; the inscription clears the same ground at 3.31 against 3.3, so the order of laying over decides that entry too.
- **Response:** fixed, in the intent first. INT-0003 criterion 3 now says which ground each carved stop is held on: both on the page as it lies, the top stop on the stone as well, and that the foot stands at 2.80 at the stone's brightest. The colour the owner approved is kept; the owner has been told a lift to `#c21b1b` would clear it. T-203 pins the order of laying over and compares without rounding.

### C-002: The void's bound names neither its lettering roles nor its grounds, and one pairing fails
- **Where:** `build-plan.md` T-203; INT-0003 criterion 3
- **Failure mode:** EARS-vague
- **Why it matters:** the void has four grounds and three lettering roles; subdued text on the tinted row of a sunken ground is about 4.46. The entries are written by the theme's author, and nothing checks that every ground a role is set on is listed.
- **Response:** fixed. T-203 names each pair the theme must hold. The tinted row is a ground of its own, on which only the void's text and accent are set; the stylesheet sets no subdued text there. A new test, `test_every_text_on_ground_pair_is_promised`, fails when a rule sets a text token on a ground token that no entry covers.

### C-003: The browser's measure of contrast sees only flat grounds
- **Where:** `build-plan.md` T-211
- **Failure mode:** plan-test-mismatch
- **Why it matters:** text that sits on the page is measured against `#0a0708`, never the stone's sheen; a ground made by a gradient, letters with a gradient clipped to them, and a visited link cannot be measured at all.
- **Response:** fixed. T-211 gains clauses: when the nearest ground is the page, the stone's brightest tone and the glow are laid over it from the theme file; an element whose ground is an image, or whose colour is clear, is refused and not measured wrongly. Clipped letters and visited links are held by the theme file's entries alone, and the plan says so.

### C-004: INT-0006 criteria 4 and 5 have no verification for most parts
- **Where:** `build-plan.md` T-206, T-207, T-208
- **Failure mode:** intent-drift
- **Why it matters:** contrast is tested for the button, the field and text in containers only, and the keyboard only as Tab reaching the controls.
- **Response:** fixed. One list of the parts (`tests/parts.py`) says of each whether it carries text, takes the keyboard, and which states it has. Three tests run over the whole list: contrast for every part that carries text, in each state; the keyboard reaching and marking every part that takes it; and each control being worked by its keys.

### C-005: The tasks that lay the stone and dress the ornaments do not measure them
- **Where:** `build-plan.md` T-204, T-205; INT-0003 criteria 1 and 4
- **Failure mode:** EARS-vague
- **Why it matters:** nothing shows the stone is drawn, lies behind the content, or is no brighter than the theme file's bound; the ornaments are named and not measured; the stillness and print tests would pass on a stylesheet with no animation and no ornament.
- **Response:** fixed. T-204 gains clauses for the stone's layer (it exists, is fixed, lies beneath, ignores the pointer, takes its opacity from the token) and a test that a picture of the bare stone has no pixel brighter than the bound. T-205 gains a clause for each ornament, and a test that animations do run when stillness is not asked for.

### C-006: A dialog worked by script contradicts INT-0001, whose criterion 4 is traced to tests of the README
- **Where:** `build-plan.md` T-210; INT-0001
- **Failure mode:** intent-drift
- **Why it matters:** the showroom is the page that shows the look and it runs script, one piece of which INT-0001 names as left out; criterion 4 was traced to tests that do not look for script.
- **Response:** fixed, in the intent first. INT-0001's boundary and criterion 4 now say the kit needs no script and that the showroom's play is apart from it. Criterion 4 is traced to the tests that look for script. The modal dialog moves into the furniture without script (a button's `commandfor` with `command="show-modal"`), tested with script off; it is dropped from T-210.

### C-007: The check that the kit holds no script looks only at file names
- **Where:** `build-plan.md` T-210; `test_kit_holds_no_script`
- **Failure mode:** plan-test-mismatch
- **Why it matters:** half the clause was not measurable; the test missed script inside HTML and SVG, and nothing held the showroom out of a release.
- **Response:** fixed. The clause says what is tested: no tracked HTML or SVG outside `showroom/` holds a script element, a handler attribute or a `javascript:` address; every page that proves the furniture is opened with script off; the bundle's test asserts the exact set of names. INT-0006 records the standing of `examples/`.

### C-008: Tasks change files that existing tests pin, and those tests are not in their Touches
- **Where:** `build-plan.md` Touches of T-201, T-202, T-203, T-212, T-213
- **Failure mode:** hidden-dep
- **Why it matters:** each would fail the guards at its own commit.
- **Response:** fixed. `tests/common/mod.rs`, `tests/test_fetch_release.py`, `tests/test_release.py` and `tests/test_readme.py` are added where they are changed. The guard script is no longer touched: its checks reach the look through `check` and the tests. The README's words leave T-212 and are all in T-214.

### C-009: Several clauses lean on work that a later task, or no task, makes
- **Where:** `build-plan.md` T-201, T-203, T-204, T-208
- **Failure mode:** hidden-dep
- **Response:** fixed. T-201 adds `look --check` as a command that reads and judges the theme file, so its refusals can be run in its own commit. T-203 touches the form's write-up and the parser. T-204's tests take each stylesheet as it comes to exist. T-208 names the page it opens, `tests/pages/every-part.html`.

### C-010: The Execution Sequence is not in the order of execution
- **Where:** `build-plan.md` Execution Sequence
- **Failure mode:** hidden-dep
- **Response:** fixed. T-216 stands first and says nothing is pushed before its first entry; T-215 follows it; T-211 stands before T-204.

### C-011: The cut order cannot be carried out as written, and it cuts what the sprint was begun for
- **Where:** `build-plan.md`, the paragraph before the Execution Sequence
- **Failure mode:** missing-risk
- **Why it matters:** later tasks and three tests demand every part, so a cut leaves the guards failing; and the order removed play first.
- **Response:** fixed. Nothing is cut without the owner's word. The tests read the one list of parts, so a cut is one recorded change with an amended INT-0006. What is offered first, if the sprint will not fit, is the door's picture, then the plaything, then parts from the end of the list. INT-0007 gains a criterion for play.

### C-012: The sprint's largest judgement comes last, and two things it needs have no task
- **Where:** `build-plan.md` T-209; `test-plan.md` "By review"
- **Failure mode:** missing-risk
- **Response:** fixed. T-209 ends with a review: the owner is shown the showroom before T-210, T-213 and the front page's tasks begin. T-209 builds the side by side of the fixed-pitch families as a part of the showroom. The designer's unread word is recorded as left to the owner.

### C-013: The Pages workflow's permission clause forbids what publishing needs
- **Where:** `build-plan.md` T-213
- **Failure mode:** EARS-vague
- **Response:** fixed. The clause names the three permissions, the identity token among them. Publishing waits on a repository variable the owner sets when Pages is on, so `main` shows no failed run before then.

### C-014: The live showroom's check is unlocked by nothing that is tracked
- **Where:** `test-plan.md` End-to-End Tests
- **Failure mode:** e2e-drift
- **Response:** fixed. Backlog task T-104 under INT-0007 carries the live check and says what it must find. The test plan names it, and the section's status now reads as it is.

### C-015: Version 0.2.0 is set while 0.1.0 has never been tagged, and two criteria of INT-0005 are touched without trace
- **Where:** `build-plan.md` T-212; INT-0005
- **Failure mode:** missing-risk
- **Response:** fixed. INT-0005 and backlog task T-102 record the commit `v0.1.0` is tagged at once `main` moves on. T-212 gains clauses and tests for criteria 4 and 6 with the look's files, and touches the release workflow's notes.

### C-016: Tests without a clause, and tests weaker than their clause
- **Where:** `test-plan.md`
- **Failure mode:** plan-test-mismatch
- **Response:** fixed. The bundle's same-bytes test has a clause; the heading test runs over all five settings; the colours' test says what a drawing's own colours are; T-211 gains a clause for opening a page with script off.

### C-017: "Every state" is narrowed to two parts, and nothing says how a state is shown or brought about
- **Where:** `build-plan.md` T-209, T-206; INT-0006 criterion 2
- **Failure mode:** EARS-vague
- **Response:** fixed, in the intent first. INT-0006 criterion 2 now tells states that hold at rest, which the showroom shows, from states a hand brings about, which it leaves to the visitor and the tests bring about; the showroom imitates none, so it adds no rule of its own. The plan lists each part's states, names the attribute that marks a fault, says the helper waits out transitions, and excludes the open list of a choice by name.

### C-018: The dark blood is a role and a risk that stand only in Notes
- **Where:** `build-plan.md` T-201, T-206; INT-0003, INT-0004
- **Failure mode:** missing-risk
- **Response:** fixed. INT-0003 names the blood as a role and where it came from. The edge a part filled with blood carries is a role too, held at 3 or more against the ground beside it by an entry in the theme file and by a test in the browser.

### C-019: T-201 does not say which roles and measures the form requires, nor that a font it names is one the kit holds
- **Where:** `build-plan.md` T-201; INT-0004
- **Failure mode:** EARS-vague
- **Response:** fixed. T-201 lists the roles and the measures by name, and refuses a family the kit does not hold. INT-0004 records the four roles and that a heading names either a role or a family of the kit.

### C-020: T-214 is three pieces of work, and its door is a second drawing of the furniture
- **Where:** `build-plan.md` T-214; INT-0007 criterion 5
- **Failure mode:** granularity
- **Response:** fixed. It is split into the words (T-214), the door (T-217) and the colours' source (T-218). A drawing's own colours are defined as the briar's squares and the statue's maps. The words name the new folders and the new command. INT-0007 says the door is a drawing and not a capture.

### C-021: How a page takes the look on is settled only in the build plan's prose
- **Where:** `build-plan.md`; INT-0001, INT-0005
- **Failure mode:** intent-drift
- **Response:** fixed, in the intents. INT-0003 names the four files, the rule against imports and paths, and how rules are scoped and why. INT-0005 says what a release holds from the one that first holds the look. INT-0001's list of what the first version holds is brought up to date. T-204 defines how a rule inside an at-rule is read.

### C-022: INT-0002 is planned against without being reviewed, and T-215 drops half of the task it takes up
- **Where:** `research-report.md`; `build-plan.md` T-215
- **Failure mode:** intent-drift
- **Response:** fixed. The research report lists INT-0002. T-215's clause and its review record INT-0001 criterion 1 as well.

## Confidence
block

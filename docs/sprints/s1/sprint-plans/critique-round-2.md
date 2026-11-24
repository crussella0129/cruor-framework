# Plan Critique — Sprint 1, second round

The critic checked each response of the first round against the files. It
found eleven of the twenty-two concerns closed as the responses said, and
raised what was left of the others again, with what the rewrite had newly
broken. Its concerns are given here each cut to its label, where it stands
and why it matters, and followed by what was done. Its verdict was `block`,
resting on C-001 to C-004; it called C-005 to C-013 caveats. The plans were
amended and reviewed a third time; the last round is in `critique.md`.

## Concerns

### C-001: The rise's row in the table of parts cannot pass the tests that run over the list
- **Where:** `build-plan.md`, the table of parts; T-206, T-209
- **Failure mode:** plan-test-mismatch
- **Why it matters:** a rise that is hidden at rest cannot be visible; Tab lands on its button and not on it; the kinds of a notice and of a badge had no way of being asked for.
- **Response:** fixed. The rise's state at rest is a `<dialog open>`; being shown from its button, as a popover or as a modal dialog, is a state a hand brings about; what takes the keyboard is its button and what is inside it. A kind is asked for by `data-kind`, which needs no class of its own.

### C-002: T-211's page with a script in it fails T-210's check that no tracked page holds one
- **Where:** `build-plan.md` T-211, T-210
- **Failure mode:** hidden-dep
- **Response:** fixed. The pages T-211's tests open are written by the tests into a temporary folder and are not tracked.

### C-003: T-202 leaves the stone out of the tokens that T-204 then needs
- **Where:** `build-plan.md` T-202, T-204
- **Failure mode:** hidden-dep
- **Response:** fixed. T-202 makes a token of each of the stone's four keys; T-204 names them.

### C-004: "Its text at 4.5" does not say which text, and shuts out the look's own large lettering inside a part
- **Where:** `build-plan.md` T-206, T-207, T-208
- **Failure mode:** EARS-vague
- **Why it matters:** a paragraph in a container is an inscription, held at 3.3 and not 4.5, and a masthead's title is carved; the clause forced every part into bone or into a refusal.
- **Response:** fixed. The table of parts, and so `tests/parts.py`, says for each part which text is measured and at which of INT-0003's bounds. T-207's clause covers a paragraph in every container that can hold one. The blood is never a ground for lettering, which the static check of promised pairs would catch.

### C-005: The helper still misreads a ground that is partly clear, or laid by a pseudo-element
- **Where:** `build-plan.md` T-211
- **Failure mode:** plan-test-mismatch
- **Response:** fixed, by a different means. The ground behind lettering is read from a picture of the page with the lettering made clear, so a tint, a gradient and a pseudo-element's fill are read as they are drawn. Colours are read with stillness asked for, so nothing is in passage and an endless animation is not running.

### C-006: The stone's pixel test allows more than the inscription's margin, and nothing says what follows if it fails
- **Where:** `build-plan.md` T-204
- **Failure mode:** missing-risk
- **Response:** fixed. The test now holds every entry on `stone` against the brightest pixel of a picture of the bare stone, with no allowance, at a fixed size and with the candle at its strongest. If it fails the build stops and the owner chooses; no bound is loosened.

### C-007: The dialog now rests on a newer thing than any other part, and the research still says it cannot be done
- **Where:** `build-plan.md` T-207; `furniture-survey.md`; INT-0006
- **Failure mode:** missing-risk
- **Response:** fixed. The survey is corrected and the source is in the research report, in place of one on a method that was not chosen. INT-0006's Consequences record which parts rest on newer things and what a visitor without them meets. Other engines are carried by backlog task T-105, named in the test plan.

### C-008: The check that every pair is promised sees only a rule that sets both colours itself
- **Where:** `build-plan.md` T-203
- **Failure mode:** plan-test-mismatch
- **Response:** fixed. The plans say plainly that a pair no single rule sets is held by the tests over the list, which measure what is drawn. An entry naming a role or ground the theme does not have is refused, with a test.

### C-009: The owner's acceptance of 2.80 is recorded as silence
- **Where:** INT-0003 criterion 3 and Consequences
- **Failure mode:** intent-drift
- **Response:** fixed. The question is put to the owner when the showroom first stands, as one of four things asked there, and INT-0003 says its criterion is amended to their answer.

### C-010: The intents still say things the rewrite has overtaken
- **Where:** INT-0007, INT-0004, INT-0001, INT-0005
- **Failure mode:** intent-drift
- **Response:** fixed. INT-0007 names the repository variable and says what the showroom holds as INT-0006 does; the evidence lines point at the tasks as now numbered, and a history entry corrects the one that named T-214 for the door; INT-0005 words the tag's place as what holds if `main` moves on first.

### C-011: T-218 and a clause of T-204 cite INT-0004 criterion 2 for what it does not say
- **Where:** `build-plan.md` T-218, T-204
- **Failure mode:** intent-drift
- **Response:** fixed, in the intent. INT-0004 gains criterion 6, which states the promise. T-218 brings the script's four families under it as well as its colours; the sizes the picture sets its words at are left as the picture's own, with the reason.

### C-012: The paragraph on cutting covers parts, not the two things offered first
- **Where:** `build-plan.md` "Cutting"; T-218
- **Failure mode:** hidden-dep
- **Response:** fixed. T-218 rests on T-214 and not on the door. The paragraph says which criterion of INT-0007 each of the first two cuts leaves unmet or half met, and that a cut part changes the list and the test that pins it together.

### C-013: Four small gaps between clauses and their tests
- **Where:** `build-plan.md` T-201, T-206; `test-plan.md`
- **Failure mode:** plan-test-mismatch
- **Response:** fixed. A heading set by a family's name is tested as taken; `seal-font` falls under the same refusal; the list marks which parts the blood fills and the edge is tested on each; an empty field's placeholder is the lettering measured.

## Confidence
block

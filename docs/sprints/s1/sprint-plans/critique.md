# Plan Critique — Sprint 1

Third review, of both plans, the intents, the research and the backlog as
they stood after the second round. The critic checked each response of
`critique-round-2.md` against the files and found all thirteen
second-round concerns closed. It found that every EARS clause has a named
test and every named test a clause, that the Execution Sequence follows
the declared dependencies, that no existing test a task would break is
missing from its Touches, and that no two clauses contradict one another.
It raised six caveats, none of which it held would by itself keep the plans
back.

Each concern is given here cut to its label, where it stands and why it
matters. The line marked **Response** is the planner's and says what was
done; all six were answered in the plans and the intents before the lock.

## Concerns

### C-001: "Made clear" does not say what becomes of the lettering's own glow, nor what the box of a control's lettering is
- **Where:** `build-plan.md` T-211 third clause
- **Failure mode:** EARS-vague
- **Why it matters:** lettering made clear still casts its shadow, so the inscription's glow would be read as ground and could decide the answer; a field and a choice have no element for their lettering, so the box would be the control's.
- **Suggested response:** fix-in-plan.
- **Response:** fixed. The lettering's own shadow is taken off with its colour, and the plan says why: the glow is the letter's own light and not the ground it stands on. The box is the rectangles of the text itself, or the content box of a control that has no element for its text.

### C-002: The readings lean on three things that no clause checks
- **Where:** `build-plan.md` T-211, T-204, T-205, T-208
- **Failure mode:** plan-test-mismatch
- **Why it matters:** stillness stops a passage between two colours only if the stylesheets remove transitions under it; that the still candle is the candle at its strongest was assumed; the helper's own working of `stone` was pinned to no value.
- **Suggested response:** fix-in-plan.
- **Response:** fixed. T-205 and T-208 hold that under stillness nothing has a transition of any length; T-204 holds that no step of the candle's flicker is stronger than the candle when still; T-211 pins the worked value of `stone` and the inscription's ratio on it, the same values the tool's test pins.

### C-003: Carved letters inside a part with a ground of its own are promised nowhere
- **Where:** `build-plan.md`, the table of parts, and T-203; INT-0006 criterion 4
- **Failure mode:** plan-test-mismatch
- **Why it matters:** the entries for carved letters name the page and the stone only, and a browser cannot measure them, so a heading in a container was held by nothing; the foot stop stands at about 2.94 on the sunken ground.
- **Suggested response:** fix-in-plan.
- **Response:** fixed. The masthead has no ground of its own and lies on the page. A heading set in a container that has a ground of its own is not carved: it is lettered flat in the inscription's colour and measured there at 3.3, with a clause in T-207 and a test. INT-0006 criterion 4 says so.

### C-004: A part that cannot be used is held at 3, which INT-0006 does not say
- **Where:** `build-plan.md` T-206 third clause; INT-0006 criterion 4
- **Failure mode:** intent-drift
- **Suggested response:** fix-in-plan, in the intent.
- **Response:** fixed, in the intent. INT-0006 criterion 4 states the bound for a part that cannot be used, and the reason.

### C-005: The new criterion of INT-0004 is worded more strictly than the plans can meet, and the plan's own lines have not caught up with it
- **Where:** INT-0004 criterion 6; `build-plan.md` Intents line, T-204
- **Failure mode:** intent-drift
- **Why it matters:** the stone's surface and the sigil are drawn in `data:` addresses inside the stylesheet, which cannot read a token, so read to the letter the criterion would be unmet.
- **Suggested response:** fix-in-plan.
- **Response:** fixed. Criterion 6 counts the drawings a stylesheet holds in a `data:` address among a drawing's own colours. The build plan's Intents line reads 1 to 6, T-204 links INT-0004, and the evidence lines of INT-0003, INT-0001 and INT-0005 name the tasks that now carry a criterion.

### C-006: What the owner's answers at T-209 may change is in no task's Touches
- **Where:** `build-plan.md` T-209, T-203, T-218
- **Failure mode:** hidden-dep
- **Suggested response:** fix-in-plan.
- **Response:** fixed. T-209's Touches name the theme file, the tokens and INT-0003 as changed only on the owner's answer. T-218's name the door's picture if it exists, and its Notes say it follows T-217 in the sequence when both are built.

## Confidence
proceed-with-caveats

# INT-0007 — The showroom

<!-- sprint-loop-intent-v2 -->
- **Intent ID:** INT-0007
- **State:** active
- **Work evidence:** [T-209, T-210, T-213 and T-217, Sprint 1 build plan](../sprints/s1/sprint-plans/build-plan.md)
- **Completion evidence:** none
- **Code evidence:** none
- **Test evidence:** none
- **Documentation evidence:** none

## Intent

The framework has a showroom: a page built from the kit and from nothing
else, where a visitor sees Cruentous Atonement
([INT-0003](INT-0003-cruentous-atonement-look.md)) and every piece of
furniture ([INT-0006](INT-0006-the-furniture.md)) in use, and can try them.

The designer whose reading began this (see INT-0006) asked for "some more
play", "some more world, some more place". The front page is a picture: it
can be looked at and nothing in it can be touched. The showroom is the
answer to that. It is a place a visitor is in, laid out as a real page
would be, where a button can be pressed, a field written in and a part
opened; it is not a catalogue with one of each thing in a row.

It also proves the kit. If the showroom can be built from the framework's
stylesheets and plain HTML alone, so can another person's page.

What it holds:

- the look on a whole page: the stone, the inscription, carved headings and
  the ornaments;
- every part of the furniture, in every state it has at rest, used where
  such a part would be used; the states a hand brings about are the
  visitor's to bring about ([INT-0006](INT-0006-the-furniture.md)
  criterion 2);
- how each is written, close by, so that a visitor can take it;
- the framework's own world, as its front page has it: the statue weeping
  blood, seen from more than one angle, and the stem of bloody thorns. The
  owner named this manner a "renaissance grotesque" on 24 November 2026.

Boundaries:

- It links the framework's stylesheets as any page would, and adds none of
  its own beyond what lays out the showroom itself.
- Its pictures are its own, kept in its folder and drawn from the same
  maps as the front page's. They are no part of the kit or of a release,
  and the photographs they were made from are credited on the page.
- It may hold script for the sake of play, which the kit itself may not.
  The owner settled this on 24 November 2026 ("Wherever it helps"). The
  script is the showroom's own and is no part of a release. With script
  turned off the page still shows every part.
- It is served on the web by GitHub Pages, which the owner chose the same
  day, and can always be opened from a copy of the repository as well.

## Acceptance criteria

Settled in Sprint 1's Plan, 24 November 2026:

1. One page in the repository shows the look and every part of the
   furniture in use, and opens from a copy of the repository with no build
   step.
2. It links only the framework's own stylesheets and fonts, and fetches
   nothing from anywhere else.
3. Beside each part is the HTML that makes it.
4. A check opens it in a browser and finds every font loaded, no failed
   request, and every part present.
5. The front page points to it through a door: a picture that is a link
   to it. The door is a drawing in the look's colours, made by the script
   that draws the front page; it is not a capture of the showroom.
6. The owner judges by eye that it is a place and not a list.
7. With script on, a visitor can play: there is at least one thing in it
   that answers the hand as matter would, and a part's HTML can be taken
   with one press.
8. It carries the front page's world: the statue weeping blood from at
   least two angles, and the stem of thorns. The owner judges by eye that
   it is a place of that kind.

## Rationale

A look is judged by being in it. A person deciding whether to take the kit
wants to see a page made with it and to try its parts, before reading how.

## Alternatives

- **Show the parts on the front page alone.** The front page is a picture
  and cannot be tried.
- **A catalogue: each part once, in a grid.** It shows what exists and not
  what a page made of it is like, which is what was asked for.

## Consequences

- Serving it on the web needs two things only the owner can do: GitHub
  Pages turned on for the repository, and the repository variable
  `SHOWROOM` set to `published`. Until both are done the workflow runs its
  checks and publishes nothing, and the door on the front page leads to an
  address that does not yet answer. Backlog task T-104 carries the check
  that it is live.
- What a visitor sees on the web is the showroom of the default branch, not
  of a release.
- The owner named a second statue for the showroom and the front page on
  24 November 2026: the thinker, "darker, pixelated, and crying blood",
  for its pose and the angles it offers. It is made as the first was, from
  photographs whose licence allows it, once the owner has chosen them
  (Sprint 1, T-221).
- The front page's picture is drawn from words
  (`assets/readme/text.md`); a picture of the showroom in it is a new kind
  of thing for `tools/draw_readme.py` to place.

## Transition history
- 2026-11-24: created as `proposed` in Sprint 1's Research, from a
  designer's reading of the front page and the owner's choice that day.
- 2026-11-24: `proposed` to `planned`. The owner settled that the showroom
  may hold script and is served by GitHub Pages, and approved Sprint 1's
  plan, which builds the page (T-209), its play (T-210), its publishing
  (T-213) and the front page's door to it (T-214).
- 2026-11-24: revised after the plan's first review, still `planned`.
  Criterion 5 says what the door is; criterion 7, for play, is new.
- 2026-11-24: revised after the plan's second review, still `planned`. The
  door to the showroom is task T-217 of the plan as rewritten, not T-214 as
  the entry above says. What the showroom holds follows INT-0006's
  criterion 2, and the Consequences name what the owner must do for it to
  be served.
- 2026-11-24: `planned` to `active`. Sprint 1's Build reached T-209, and the showroom stands: one page built from the kit alone, which opens from a copy of the repository.
- 2026-11-24: revised at the owner's word, still `active`. Shown the
  showroom, the owner judged it a place and not a list ("Yes, a place"),
  which is criterion 6. Of its look they said: "We want a place with that
  kind of aesthetic", meaning the front page's "renaissance grotesque":
  "the david statue crying blood from dramatic angles and the stem of
  bloody thorns". Criterion 8 is new, and the showroom is given pictures of
  its own (Sprint 1, T-220). The same day they named a second statue, the
  thinker (T-221).
- 2026-11-24: revised at the owner's word, still `active`. The owner found
  that the blood on the statue did not keep to the face. It is now worked
  out from the carving's surface and gravity, let out where the owner
  marked the corners of the eyes and held near the ways they drew, and
  from the middle of the lower lid it wells along the lid before it falls.
  Shown the result, the owner said: "Yes, it's right". Both pictures, the
  front page's and the showroom's, were drawn again from it (Sprint 1,
  T-222).
- 2026-11-24: revised at the owner's word, still `active`. The owner found
  that the blood did not run far enough down the face, nor drip. Each
  stream now goes on down the face along the carving and ends in a drop.
  On the front view, the clotted spot beside the nose is gone; it is where
  a run from the lid's stream and a run from the inner corner's stream
  meet. Shown the result, the owner said: "looks good in the after photo"
  (Sprint 1, T-223).
- 2026-11-26: revised at the owner's word, still `active`. Set beside the
  pictures on `main`, the new ones were busier and darker, and the owner
  said: "the old ones look great". The statue's two maps are again those
  on `main`, and the pictures drawn from them are as they were before
  T-222 (Sprint 1, T-224).
- 2026-11-26: criterion 5 built, still `active`. The front page is now two
  pictures: the page, and beneath it a door that is a link to the showroom.
  The owner shaped the door: an arch carved of the damned, with David's
  head face on as its crest and a split down its middle; blood boiling
  through the doorway, and the door and two candelabras with skulls on
  floating stone ledges with bats' wings. "No this is the direction"
  (Sprint 1, T-217). The head is drawn from a photograph of a plaster cast
  by Palnatoke, offered under CC BY-SA 3.0, and the front page says so.
- 2026-11-26: revised at the owner's word, still `active`. The showroom
  now opens with the same door: the head's eyes bleed, its mouth opens and
  pours, the door splits open on the light and the view goes in. A picture
  on GitHub cannot answer a press, so the front page's door stays still
  and the showroom plays this on arrival. It runs only with script, never
  for a visitor who asks for less motion or who is sent to a room, and a
  press, a key or the wheel ends it; without it the showroom is as it was
  (Sprint 1, T-225).

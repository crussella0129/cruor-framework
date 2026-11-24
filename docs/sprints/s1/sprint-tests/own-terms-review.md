# The own-terms review: a record

[INT-0001](../../../intents/INT-0001-the-cruor-framework.md) criterion 5:
nothing in this repository or its history names another typeface or
describes Cruor by comparison with one. Task T-216 keeps that, as T-013 did
in Sprint 0, by a review made before every push, from outside the
repository, because a check kept here would have to hold the names it
forbids. Sprint 0's record is
[its own file](../../s0/sprint-tests/own-terms-review.md); this one carries
on from its eleventh entry.

How each review is made:

- For every commit the push carries, the content of every file the commit
  adds or changes, the file's path and the commit's message are searched
  for the names of other typefaces. The list of names is kept outside the
  repository.
- Font files are opened with fontTools. Every string of each font's name
  table and every glyph name is searched, and each font's WOFF2 metadata
  block and private block is read, or noted as absent.
- The new prose of those commits is read once for any description of Cruor
  by comparison with another typeface. Lines holding the words that usually
  mark a comparison are picked out for that reading.
- The files each commit adds or changes are set against what the commit's
  task touches.
- The entry is added before the push and covers every commit the push
  carries. A commit whose only change is a new entry in this file is
  covered by the entry it adds; it is searched after it is made, and
  nothing is pushed if anything is found.
- The text of a pull request is searched before it is opened.

## Entries

### 1. 24 November 2026, at the start of Build, before anything of the sprint is pushed

- **Commits covered:** `4d8e264fa708b5512e9138e2322840b1fee44987` to
  `b86041169a183560d754509eb0ef2d53b508c632`, five commits: the two merges
  GitHub made of Sprint 0's pull requests, which are already in the default
  branch and reach the work branch here; the sprint's start and research;
  its plans, with the three reviews of them; and the lock.
- **Also covered:** nothing; no font file is in the commits.
- **Pull requests:** two, both Sprint 0's own, both merged. None of the
  updater's, open or closed.
- **Found:** none. The three critiques are another reader's words, cut to
  their substance; the critic was asked beforehand to name no other
  typeface, and they were searched with the rest.
- **Read for comparisons:** no line was picked out. The research names a
  video game and a kit of components that a designer and the owner pointed
  to; neither is a typeface, and Cruor is set beside neither. The plans say
  which family of Cruor sets the title, the headings, the text and code,
  and describe no letter.
- **Files against tasks:** the three commits of the sprint change the Book
  alone and belong to no task of the Build.
- **Not pushed yet.** This entry is the work of T-216 and is committed by
  the helper that commits a task, which makes a second commit of its own to
  record the first. Those two commits are covered by the next entry, and
  the first push of the sprint follows that one.

### 2. 24 November 2026, in Build, before the sprint's first push

- **Commits covered:** `b44d52904b02e5b46601f996d12123c4fab9decb` to
  `24df4b0aa29b09da8d8cfe95fb0924cbc6cc7c1c`, ten commits: the five tasks
  done so far (T-216, T-215, T-201, T-202 and T-203), each with the commit
  the helper makes to record it. With the five of entry 1 they are the
  fifteen this push carries, and all fifteen were searched again as one.
- **Also covered:** nothing; no font file is in the commits. The theme file
  names four families, each one of Cruor's, and the tool refuses a family
  the kit does not hold.
- **Pull requests:** as entry 1 tells.
- **Found:** none.
- **Read for comparisons:** no line was picked out. The write-up of the
  theme file's form says what each family sets (the title, the headings,
  running text, code) and describes no letter.
- **Files against tasks:** T-216 changes this file. T-215 changes the
  intents INT-0002 and INT-0001. T-201 adds `look/theme.toml`,
  `look/THEME.md`, `src/theme.rs` and its tests, and changes `src/main.rs`
  and `tests/common/mod.rs`, as its task lists. T-202 adds `src/look.rs`,
  `look/tokens.css` and `tests/look.rs`. T-203 adds `src/contrast.rs`,
  `tests/contrast.rs`, `tests/stylesheets.py` and
  `tests/test_promised_pairs.py`. One file falls outside a task's list:
  T-202 changed `tests/theme.rs`, a test of T-201, because the check it
  runs came to cover the tokens as well; and T-203 changed
  `tests/test_theme_form.py` for the same kind of reason, and added
  `tests/stylesheets.py`, which its list did not name. Each of the ten
  helper commits changes a ledger of the Book alone.
- **A slip in a ledger.** The ledger gives T-215 as completed at 05:14 and
  T-201 at 05:12, though T-215 was done first; the two times before T-201's
  were written by hand and are a few minutes out. The ledger is append-only
  and is left as it is.

### 3. 24 November 2026, in Build, when the look's stylesheet is done

- **Commits covered:** `59a231490fffc213cb0aea35b1102b76bc8c3a1b` to
  `5e6dd5f71e0516d26420b7d7e431293441481635`, six commits: T-211, T-204 and
  T-205, each with the commit the helper makes to record it. The commit
  that recorded entry 2 (`8cdd2be`) changes this file alone and was pushed
  with it.
- **Also covered:** nothing; no font file is in the commits. The look's
  stylesheet names no family: each is asked for by a token, with a generic
  word (`serif`, `sans-serif`, `monospace`) to fall back on.
- **Pull requests:** as entry 1 tells.
- **Found:** none.
- **Read for comparisons:** no line was picked out. The stylesheet's
  comments tell what each rule draws (the stone, the candle, a carved
  heading, the seal, the sigil) and set Cruor beside nothing.
- **Files against tasks:** T-211 adds `tests/browser.py` and
  `tests/test_browser_means.py`; it did not need to change
  `tests/helpers.py`, which its list named. T-204 adds
  `look/cruentous-atonement.css`, `tests/test_look_css.py`,
  `tests/test_look_ground.py` and `tests/pages/bare.html`. T-205 changes the
  stylesheet and `tests/test_look_css.py`, and adds
  `tests/test_look_page.py` and `tests/pages/plain.html`.
- **CI for the first push.** Run
  [45332407479](https://github.com/crussella0129/cruor-framework/actions/runs/45332407479) for
  `8cdd2be1aa9701542c0c2e48ac19b1aa6b49e07f` concluded `success`.

### 4. 24 November 2026, in Build, when the furniture is done

- **Commits covered:** `8e4268925ae2139255c76381555b3ef1071e82e7` to
  `bd67c850b2d23d1db012428e040b2a02e9bc2e93`, six commits: T-206, T-207 and
  T-208, each with the commit the helper makes to record it. The commit
  that recorded entry 3 (`b5c2935`) changes this file alone and was pushed
  with it.
- **Also covered:** nothing; no font file is in the commits. The
  furniture's stylesheet names one family only by token, for the seal.
- **Pull requests:** as entry 1 tells.
- **Found:** none.
- **Read for comparisons:** no line was picked out. The stylesheet's
  comments tell what each part is and how it is asked for.
- **Files against tasks:** T-206 adds `look/furniture.css`,
  `tests/parts.py`, `tests/test_furniture.py` and
  `tests/pages/controls.html`. T-207 and T-208 add to the first three and
  add `tests/pages/containers.html`, `tests/pages/pieces.html` and
  `tests/pages/every-part.html`. Four changes fall outside a task's list.
  T-206 changed `tests/browser.py` and `tests/test_browser_means.py`, of
  T-211: the measure had to learn that a field the keyboard comes to has
  its words selected. T-207 changed `tests/browser.py` again, so that a
  page is asked for a second time when this machine's own server refuses
  one connection; and it changed `look/cruentous-atonement.css` and
  `tests/test_look_page.py`, of T-205, for the reason given next.
- **A change to the look, found by measuring it.** A quotation had a faint
  tint behind its text, as the look had where it was first made. Laid over
  the stone at its brightest, that tint brings running text below the 3.3
  the look promises. The tint is gone, and the quotation's channel is now
  its border, so that its text lies on the page and is held against the
  page at its brightest. A test of plain lettering on the page was added
  with it, beyond what the plan named.
- **CI for the second push.** Run
  [45333909481](https://github.com/crussella0129/cruor-framework/actions/runs/45333909481)
  for `b5c2935fd6c3ff454b3a1b494c1d7d2d778d5a65` concluded `success`.

### 5. 24 November 2026, in Build, when the showroom first stands

- **Commits covered:** `e559965f7aa7e1fd6b5cce4dc02abc6efee2a2f9` and
  `c579a209afa2f600c863cb7c026391f13cb96b23`, two commits: T-209 and the commit
  the helper makes to record it. The commit that recorded entry 4
  (`6d6b425`) changes this file alone and was pushed with it.
- **Also covered:** nothing; no font file is in the commits. The showroom
  names Cruor's families and no other: the four the look sets, and the five
  of fixed pitch set side by side.
- **Pull requests:** as entry 1 tells.
- **Found:** none.
- **Read for comparisons:** the showroom's words were read whole, since
  they are the first the kit says of itself to a visitor. They tell what
  Cruor means and where each family is used, and liken it to nothing.
- **Files against tasks:** T-209 adds `showroom/index.html`,
  `showroom/showroom.css` and `tests/test_showroom.py`, and moves
  INT-0007 to `active`. Nothing falls outside the task's list. The look and
  the theme file are not changed: whether they are waits for the owner's
  answers, which the plan asks for now.
- **How the showroom's page is made.** It was written out once by a script
  kept outside the repository, so that the HTML folded beside each thing is
  the very text of that thing. The page is the source from here on; a test
  holds each folded text against the thing it stands beside, attribute for
  attribute, and sets it alone in a page to see it drawn the same.
- **Two things the tests settle that the plan left to the build.** A thing
  that stands in a row of others is as tall as its row; set alone, it is
  given a row as tall, and what it holds is measured. A thing that rises
  is raised first in both pages, so that what is compared is the thing
  open and not a thing put away.
- **CI for the third push.** Run
  [45336850401](https://github.com/crussella0129/cruor-framework/actions/runs/45336850401)
  for `6d6b4250222b78ef77630011d2657d773edb7b2d` concluded `success`.

### 6. 24 November 2026, in Build, when a release carries the look

- **Commits covered:** `3d3eb0787b2f9e7b5c382669cb151bc751490d5a` and
  `4fe2f95e27d31715df5e2d0f288be5802c493b7a`, two commits: T-212 and the
  commit the helper makes to record it. The commit that recorded entry 5
  (`c5ee661`) changes this file alone and was pushed with it.
- **Also covered:** nothing; no font file is in the commits.
- **Pull requests:** as entry 1 tells.
- **Found:** none.
- **Read for comparisons:** no line was picked out. The release's notes
  were read: they name the fonts, the look and the theme file.
- **Files against tasks:** T-212 changes the files its task lists, and one
  more: `src/main.rs`, where the help for `--tag` gave `v0.1.0` as the tag
  of the framework's version. It now says what such a tag is and names no
  version.
- **Out of the queue's order.** T-212 was built before T-210. The plan
  holds T-210, T-213, T-214, T-217 and T-218 until the owner has seen the
  showroom and answered; T-212 depends on T-208 alone and is not among
  them.
- **Tests renamed.** Two of Sprint 0's tests of the bundle took the names
  this sprint's test plan gives them: the test of what a bundle holds, and
  the test that two bundles are the same bytes. What each asserts is what
  it asserted, and more.
- **CI for the fourth push.** Run
  [45338815032](https://github.com/crussella0129/cruor-framework/actions/runs/45338815032)
  for `c5ee6617abde6e333f3200988444c6ce6d7c3025` was still running when
  this was written. Its end is told in the next entry.

### 7. 24 November 2026, in Build, a figure corrected before the owner answers

- **Commits covered:** `9845d68bbc14aa9b0b12fa6c0141a9f2f02ed55f`, one
  commit, which changes INT-0003 alone. The commit that recorded entry 6
  (`df69165`) changes this file alone and was pushed with it.
- **Also covered:** nothing; no font file is in the commit.
- **Pull requests:** as entry 1 tells.
- **Found:** none.
- **Read for comparisons:** no line was picked out.
- **What was wrong.** INT-0003's Consequences said that lifting the foot
  of a carved heading to `#c21b1b` would bring it to 3:1 on the stone at
  its brightest, and the owner had been told so. Worked out again while
  the two were being drawn side by side for the owner, `#c21b1b` stands at
  2.99 there and `#c31b1b` at 3.01. The intent now says so. The record of
  the plan's first review still gives the first figure, as it was written
  then. No colour of the look is changed: that waits for the owner.
- **Files against tasks:** the commit belongs to no task. T-209 names
  INT-0003 among what it may touch once the owner has answered; this is
  before that, and corrects what the owner is asked.
- **CI for the fourth push.** Run 45338815032, for `c5ee661`, was
  cancelled when the fifth push arrived, as the workflow does with a run
  that a newer one supersedes. Run
  [45339687942](https://github.com/crussella0129/cruor-framework/actions/runs/45339687942)
  for `df6916521378085df9be3edf3092310b984f844b`, which holds every commit
  of both pushes, was still running when this was written. This push
  supersedes it in the same way; the run for this push holds every commit
  of all three, and its end is told in the next entry.


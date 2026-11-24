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

### 8. 24 November 2026, in Build, after the owner's answers

- **Commits covered:** `650af02bf67140619dd4b3cf173dff8273c6a877` to
  `e5ccda4a98870a16d8043355b6e13ae6249f8fb1`, four commits: T-219 and
  T-220, each with the commit the helper makes to record it. The commit
  that recorded entry 7 (`48eced2`) changes this file alone and was pushed
  with it.
- **Also covered:** nothing; no font file is in the commits. Three
  pictures are new, each an SVG of squares with no letters in it. The
  statue's two carry a comment that names the sculptor, the statue and the
  photographer, and no typeface.
- **Pull requests:** as entry 1 tells.
- **Found:** none.
- **Read for comparisons:** the owner's words, as the intents now quote
  them, name Tome's theme and the manner of the front page ("renaissance
  grotesque"); they liken the place to those and Cruor's letters to
  nothing. The showroom's new words were read whole.
- **Work the locked plan does not hold.** Shown the showroom, the owner
  answered the plan's four questions. Three were answers the plan had
  ready: it is a place; code is set in Cruor Sans Pixelated; the foot of a
  carved heading is lifted. The fourth was a direction, not a yes or a no:
  the place should take after the front page as well as Tome's theme, with
  the statue weeping blood and the stem of thorns. Three tasks were added
  to the queue for this, with the owner's words in INT-0003 and INT-0007:
  T-219 (the answers, taken into the look), T-220 (the front page's world
  in the showroom) and T-221 (a second statue, which the owner named the
  same day, and which waits for photographs to be chosen). The plans stay
  as they were locked; the test report tells of these as work beyond them.
- **Files against tasks.** T-219 changes the theme file, its tokens, the
  showroom's words on which family sets code, and two tests: the
  showroom's, and the test of the masthead's briar, which had held the
  briar's stem to the colour of a heading's foot. The briar keeps the reds
  it was drawn in, and the test now says so. T-220 adds
  `tools/draw_showroom.py`, the three pictures it draws, and
  `tests/test_showroom_world.py`, and changes the showroom's page, its
  stylesheet and its first tests.
- **A fault found on the way.** On a window as narrow as a telephone's
  the ledger's table was wider than the page and pushed it sideways. It
  now moves within a place of its own, and a test holds the page still.
- **CI.** Run
  [45339913288](https://github.com/crussella0129/cruor-framework/actions/runs/45339913288)
  for `48eced2bc79ed9eb656a8c0b6b0bbc6558a0cce9`, which holds every commit
  of the fourth, fifth and sixth pushes, concluded `success`. The run for
  the fifth push (45339687942) was superseded by it, as entry 7 expected.

### 9. 24 November 2026, in Build, the showroom's site and the front page's words

- **Commits covered:** `763946444c7460e6443524f9d94735d25c52fe7f` to
  `f178781d8965ce02c33a4d76316d1b8ab61846c5`, four commits: T-213 and
  T-214, each with the commit the helper makes to record it. The commit
  that recorded entry 8 (`51aa570`) changes this file alone and was pushed
  with it.
- **Also covered:** nothing; no font file is in the commits. The front
  page's picture was drawn again from its words; it holds outlines and no
  text, and its words are searched as `assets/readme/text.md`.
- **Pull requests:** as entry 1 tells.
- **Found:** none.
- **Read for comparisons:** the front page's new words were read whole.
  They say what the kit holds and how a page takes it on, name each part
  by its class, and liken Cruor to nothing.
- **Files against tasks:** T-213 adds `tools/build-site.sh`,
  `.github/workflows/pages.yml` and `tests/test_pages.py`, and amends
  `tests/test_release.py`, as its task lists. T-214 changes
  `assets/readme/text.md`, `assets/readme/page.svg` and
  `tests/test_readme.py`, as its task lists.
- **How the workflow holds its three permissions.** The plan asks for
  exactly `contents: read`, `pages: write` and `id-token: write`. The
  workflow as a whole may only read; the job that publishes holds the
  three, and the job that runs the guards holds none of its own. The
  publishing job runs only when the repository variable `SHOWROOM` is
  `published`, so the environment Pages uses is not touched before then.
- **What the words say that is not yet so.** The showroom's address is
  given, and the words say it answers once the showroom is published. The
  fetch example still names `v0.1.0`, which no tag yet bears; both wait
  for the owner.
- **CI.** Run
  [45396756696](https://github.com/crussella0129/cruor-framework/actions/runs/45396756696)
  for `51aa570b56a46ec6396b6b52393bad8ea94d80d6` concluded `success`.

### 10. 24 November 2026, in Build, the front page takes its look from the theme file

- **Commits covered:** `52ab0c6286dbba07707d25b1a91453adf15fec0b` and
  `0ee2be2faa9e0075ff4dadfb99d9d6dfb57d46ce`, two commits: T-218 and the
  commit the helper makes to record it. The commit that recorded entry 9
  (`2451d15`) changes this file alone and was pushed with it.
- **Also covered:** nothing; no font file is in the commits. The script
  now names no family at all: it reads the four from the theme file.
- **Pull requests:** as entry 1 tells.
- **Found:** none.
- **Read for comparisons:** no line was picked out.
- **Files against tasks:** T-218 changes `tools/draw_readme.py`,
  `assets/readme/page.svg` and `tests/test_readme_pictures.py`, as its
  task lists.
- **Out of the plan's order.** The plan sets T-218 after T-217, since both
  change the script. T-218 was built first, so that the door is drawn from
  the theme file from its first line. T-217 is still queued.
- **What changed in the picture.** Code on the front page is now set in
  the family the owner chose for code, and the foot of a carved heading
  takes the lifted colour; both come from the theme file. One line of the
  stone's drawing no longer names white as its light, since white is what
  that light is when none is named. The dark line beneath a hairline takes
  the colour of shed blood, which is the nearest role to what it was.
- **CI.** Run
  [45398309163](https://github.com/crussella0129/cruor-framework/actions/runs/45398309163)
  for `2451d158c90fad93c6d7d16140fbc08938d9021f` concluded `success`.

### 11. 24 November 2026, in Build, the blood on the statue keeps to the face

- **Commits covered:** `b807f72639c053381aaad89db332b6c4ad60d8e4` and
  `2f077c003d354cd1cb3e578f7db9adc6b4e40244`, two commits: T-222 and the
  commit the helper makes to record it. The commit that recorded entry 10
  (`004dff9`) changes this file alone and was pushed with it.
- **Also covered:** nothing; no font file is in the commits.
- **Pull requests:** as entry 1 tells.
- **Found:** none.
- **Read for comparisons:** no line was picked out.
- **Files against tasks:** T-222 changes the statue's two maps in
  `assets/readme/`, the front page's picture drawn from them, the
  showroom's two pictures drawn from them, and INT-0007's history, as its
  task lists.
- **Not in the plan.** T-222 was added during the Build at the owner's
  word: the blood did not keep to the face. The way it was worked out
  stays outside the repository; only the two maps it made are in it, and
  the scripts draw from them as before.
- **CI.** Run
  [45402621356](https://github.com/crussella0129/cruor-framework/actions/runs/45402621356)
  for `004dff900732aaeca1de8672348758a9ae97a1e0` concluded `success`.

### 12. 24 November 2026, in Build, the blood runs on down the statue's face

- **Commits covered:** `d9e2186cca8ee1aa504baa4a6e348903f0224991` and
  `0bf53e34cee8ecbcb46c9cf5604f2af541813bc9`, two commits: T-223 and the
  commit the helper makes to record it. The commit that recorded entry 11
  (`22e235c`) changes this file alone and was pushed with it.
- **Also covered:** nothing; no font file is in the commits.
- **Pull requests:** as entry 1 tells.
- **Found:** none.
- **Read for comparisons:** no line was picked out.
- **Files against tasks:** T-223 changes the statue's two maps in
  `assets/readme/`, the front page's picture drawn from them, the
  showroom's two pictures drawn from them, and INT-0007's history, as its
  task lists.
- **Not in the plan.** T-223 was added during the Build at the owner's
  word: the blood did not run far enough down the face, nor drip, and the
  spot beside the nose looked clotted. As with T-222, the way it was worked
  out stays outside the repository; only the two maps it made are in it.
- **CI.** Run
  [45496486733](https://github.com/crussella0129/cruor-framework/actions/runs/45496486733)
  for `22e235ca018e52226eb12b481d084ced85fcc381` concluded `success`.


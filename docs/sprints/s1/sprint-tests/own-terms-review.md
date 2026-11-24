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


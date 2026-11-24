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


# INT-0001 — The Cruor framework

<!-- sprint-loop-intent-v2 -->
- **Intent ID:** INT-0001
- **State:** active
- **Work evidence:** [T-002, T-011 and T-013, Sprint 0 build plan](../sprints/s0/sprint-plans/build-plan.md), [T-103 backlog](../work/tasks.md), [T-207, T-210, T-212 and T-214 to T-216, Sprint 1 build plan](../sprints/s1/sprint-plans/build-plan.md)
- **Completion evidence:** [T-002, T-011 and T-013, completed tasks](../work/completed-tasks.md)
- **Code evidence:** [LICENSE-MIT](../../LICENSE-MIT), [LICENSE-APACHE](../../LICENSE-APACHE)
- **Test evidence:** [Sprint 0 test report](../sprints/s0/sprint-tests/test-report.md)
- **Documentation evidence:** [README](../../README.md)

## Intent

The Cruor framework is a public kit that gives any web page the look called
Cruentous Atonement: blood letters cut into obsidian, set in Cruor, the
owner's own typeface family. The owner, on 23 November 2026: "How about the
Cruor framework And it's everything you need to turn anything into sanguine
atonement (which might be better called cruentous atonement perhaps) theme
page (But like in the same way that sacred terminal is)". Asked whether it
is a repository of its own, they answered: "Yes, new public repo".

The model is the sacred-computer kit
([internet-development/www-sacred](https://github.com/internet-development/www-sacred)):
one public repository that holds a look's fonts, tokens and parts, which
other pages build on.

The owner's decisions, all of 23 November 2026:

- **Name and place.** The repository is `crussella0129/cruor-framework`,
  public, kept locally in a folder of the same name.
- **What the first version holds.** Cruor's web fonts with their
  `@font-face` rules ([INT-0002](INT-0002-cruor-web-fonts.md)); the look, as
  colour and type tokens and a stylesheet that plain HTML takes on
  ([INT-0003](INT-0003-cruentous-atonement-look.md)); a page that shows it
  ([INT-0007](INT-0007-the-showroom.md)); and the look written as a theme
  file ([INT-0004](INT-0004-the-look-as-a-theme-file.md)). On
  24 November 2026 the owner added the furniture, the parts a page is built
  from ([INT-0006](INT-0006-the-furniture.md)), which has a stylesheet of
  its own.
- **How pages take it in.** As versioned releases whose files a build
  fetches ([INT-0005](INT-0005-versioned-releases.md)).
- **Terms for the code.** The stylesheets, tokens, theme files and tools are
  offered under `MIT OR Apache-2.0`. The fonts have terms of their own
  ([INT-0002](INT-0002-cruor-web-fonts.md)).

Releases begin before the first version is whole. The first release,
0.1.0, holds the fonts alone, so that pages can set their text in Cruor at
once; the first version is complete with the release that first holds the
look and its theme file.

Boundaries:

- The kit has no scripted components. A page takes the look on, and uses
  every part of the furniture, with stylesheets alone. The showroom, which
  is the kit's own page and no part of a release, may hold script of its
  own for the sake of play; the owner settled that on 24 November 2026. It
  still shows everything with script turned off.
- The framework describes Cruor in its own terms. No file, comment, commit
  message or record here names another typeface or describes Cruor by
  comparison with one.
- Cruor is drawn in a project of its own, which is not public. The framework
  takes that project's built web fonts and nothing else from it.
- The first page to build on the framework is
  [Tome](https://github.com/crussella0129/Tome), a reader for mdBooks. What
  Tome does with it is Tome's own record.

## Acceptance criteria

1. The public repository `crussella0129/cruor-framework` holds this Project
   Book and a README that says what the kit is, what is in it, and how a
   page takes it in.
2. The first version holds the fonts, the tokens, the stylesheets of the
   look and of the furniture, the page that shows them and the theme file,
   each proven by its own intent.
3. `LICENSE-MIT` and `LICENSE-APACHE` stand at the root, and the README says
   which terms cover the code and which cover the fonts.
4. A page that takes the kit on needs no script: nothing the kit gives a
   page holds any, and every part works with script turned off.
5. Nothing in the repository or its history names another typeface or
   describes Cruor by comparison with one.

## Rationale

The owner was asked where Cruor's web fonts should be kept so that Tome
could fetch them when it builds, and answered with the larger thing: a kit
other pages can build on, with the fonts in it. A repository of its own lets
the kit be public while the project that draws Cruor is not.

## Alternatives

- **Keep the fonts as a release on Tome.** The question the owner was first
  asked. They chose a framework of its own.
- **Other names for the repository** (`cruor-kit`, `atonement`). The owner
  chose `cruor-framework`, the name they had been using.
- **Scripted components in the first version** (a theme picker, a dialog, a
  transformation between themes). Left out: the first version is fonts and
  stylesheets, and a larger first version would have meant writing those
  parts again from Tome's. A dialog has since become a thing a browser
  opens with no script, and is among the furniture on those terms.
- **An npm package.** See [INT-0005](INT-0005-versioned-releases.md).

## Consequences

- The framework has its own versions, and pages that build on it name the
  version they take.
- Cruor keeps growing (more characters, kerning). Each time the framework
  takes in a newer build of the fonts, that is a new version of the
  framework.
- Scripted components, if they come, are a later intent.
- The repository's tool (it writes the stylesheet of the fonts, the
  manifest and a release, and later the tokens) is written in Rust, the
  owner's usual choice. The checks that must open a font or drive a browser
  are written in Python, with fontTools and Playwright, as the project that
  draws Cruor checks its own fonts. Python alone was considered, since the
  checks need it anyway; Rust was kept for the tool because later work
  leans on it.
- Criterion 5 is kept by a review made from outside the repository before
  every push, since a check kept inside would have to hold the names it
  forbids.
- The review's record began with Sprint 0's Build, and its first entries
  left some commits out of their ranges; that sprint's test report tells
  it. The rule since: an entry is made before every push, and its range
  holds every commit the push carries, those that record an earlier entry
  among them. A pull request the owner did not write, such as the
  dependency updater's, is searched and read in the same way before it is
  merged.
- An intent whose criteria speak of what the repository holds is `realized`
  when the default branch holds it, not on the work branch's evidence
  alone. Sprint 0's test report chose this, for this intent's criterion 1
  and for [INT-0002](INT-0002-cruor-web-fonts.md).

## Transition history
- 2026-11-23: created as `proposed` in Sprint 0's Research, from the owner's
  words and their answers that day.
- 2026-11-23: `proposed` to `planned`. The owner approved Sprint 0's plan, which gives the framework its licences (T-002) and its README (T-011); the look, and so criteria 2 and 4, wait for a later sprint.
- 2026-11-23: revised after the plan's review, still `planned`. The Intent now
  says that the first release holds the fonts alone and the first version is
  whole when the look is in; the Consequences record the languages of the
  tool and its checks and how criterion 5 is kept (T-013).
- 2026-11-23: `planned` to `active`. Sprint 0's Build reached T-002, the
  licences of the code.
- 2026-11-23: Test evidence attached, still `active`. Sprint 0's Test
  phase proved criteria 1 and 3 on `dev`, and found criterion 5 met with
  a deviation the report tells: nothing in the history names another
  typeface, but for three pushes the review's entry came after the push.
  Criterion 1 is not yet true of the default branch, which waits for the
  sprint's pull request to be merged. Criteria 2 and 4 wait for the look.
- 2026-11-24: revised during Sprint 1's Plan, still `active`. The owner
  added the furniture and settled that the showroom may hold script. The
  boundary and criterion 4 now say what "no script" is held to: the kit and
  any page that takes it on, not the showroom's own play. Criterion 2 and
  the list of what the first version holds name the furniture and the
  showroom.

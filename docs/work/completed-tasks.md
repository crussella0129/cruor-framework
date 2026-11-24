# Completed Tasks Log (Append-Only)

## T-001 (sprint 0)
- **Description:** Set up the crate of the tool, the check environment, the guards and CI
- **Intent:** [INT-0002](../intents/INT-0002-cruor-web-fonts.md)
- **Completed:** 2026-11-23T18:45:21Z
- **Files modified:** Cargo.toml, Cargo.lock, rust-toolchain.toml, src/main.rs, pyproject.toml, tools/requirements.txt, tools/run-guards.sh, .github/workflows/ci.yml, .gitignore, .gitattributes, tests/cli.rs, tests/helpers.py, tests/test_guards.py, tests/test_ci.py, tests/test_repository.py, docs/intents/INT-0002-cruor-web-fonts.md
- **Commit:** `163b32002e9f7c745d6a265b2e37279d00cb720b`

## T-002 (sprint 0)
- **Description:** Add the licences of the code
- **Intent:** [INT-0001](../intents/INT-0001-the-cruor-framework.md)
- **Completed:** 2026-11-23T18:46:57Z
- **Files modified:** LICENSE-MIT, LICENSE-APACHE, Cargo.toml, Cargo.lock, tests/test_licences.py, docs/intents/INT-0001-the-cruor-framework.md
- **Commit:** `6d3fdc9d4469f3128d81f08ad406a3b72188a920`

## T-003 (sprint 0)
- **Description:** Take in the web fonts of Cruor as built at its commit 7771209, with their licence and the list of families
- **Intent:** [INT-0002](../intents/INT-0002-cruor-web-fonts.md)
- **Completed:** 2026-11-23T18:49:24Z
- **Files modified:** fonts/, tests/test_fonts_intake.py
- **Commit:** `d4fdcfea61dd128cdaf68ce17d56701f05240fff`

## T-013 (sprint 0)
- **Description:** Record the first review that keeps the repository in its own terms
- **Intent:** [INT-0001](../intents/INT-0001-the-cruor-framework.md)
- **Completed:** 2026-11-23T18:51:08Z
- **Files modified:** docs/sprints/s0/sprint-tests/own-terms-review.md
- **Commit:** `03ad4411ccd2e0ee72757634f2a1e679d62c933b`

## T-004 (sprint 0)
- **Description:** Write and check the stylesheet of the fonts from the list of families
- **Intent:** [INT-0002](../intents/INT-0002-cruor-web-fonts.md)
- **Completed:** 2026-11-23T18:54:12Z
- **Files modified:** src/main.rs, src/families.rs, src/css.rs, fonts/fonts.css, tests/common/mod.rs, tests/css.rs
- **Commit:** `ff5eebf15500bba9090599cd3309655368f33f86`

## T-005 (sprint 0)
- **Description:** Write and check the manifest of the checksums of the fonts
- **Intent:** [INT-0002](../intents/INT-0002-cruor-web-fonts.md)
- **Completed:** 2026-11-23T18:56:42Z
- **Files modified:** src/main.rs, src/manifest.rs, fonts/manifest.toml, tests/manifest.rs
- **Commit:** `a6587d99dd6f99ce9051c21d6d554a804218f4a5`

## T-006 (sprint 0)
- **Description:** Check that each font agrees with its rule
- **Intent:** [INT-0002](../intents/INT-0002-cruor-web-fonts.md)
- **Completed:** 2026-11-23T18:58:07Z
- **Files modified:** tools/check_fonts.py, tools/run-guards.sh, tests/test_check_fonts.py, tests/test_guards.py
- **Commit:** `da7b5f5f1ecd316fe4f2f2f0b2da03a36f957373`

## T-007 (sprint 0)
- **Description:** Make a page that sets a line in every face
- **Intent:** [INT-0002](../intents/INT-0002-cruor-web-fonts.md)
- **Completed:** 2026-11-23T19:01:13Z
- **Files modified:** fonts/specimen.html, tests/test_specimen.py
- **Commit:** `4e0bd53466ae397c8a8db6600a92004268fee374`

## T-008 (sprint 0)
- **Description:** Put a release together with one command
- **Intent:** [INT-0005](../intents/INT-0005-versioned-releases.md)
- **Completed:** 2026-11-23T19:04:36Z
- **Files modified:** src/main.rs, src/bundle.rs, tests/bundle.rs, docs/intents/INT-0005-versioned-releases.md
- **Commit:** `9f1b75518135175ffc4d883fa560818d911abcb5`

## T-009 (sprint 0)
- **Description:** Show a build fetching a release and checking it
- **Intent:** [INT-0005](../intents/INT-0005-versioned-releases.md)
- **Completed:** 2026-11-23T19:06:38Z
- **Files modified:** examples/fetch-release.mjs, tests/test_fetch_release.py, tests/helpers.py, tests/test_specimen.py
- **Commit:** `cfee3a045c15c218b443c2336a5b514ab3543151`

## T-010 (sprint 0)
- **Description:** Publish a release when a version tag is pushed
- **Intent:** [INT-0005](../intents/INT-0005-versioned-releases.md)
- **Completed:** 2026-11-23T19:09:25Z
- **Files modified:** .github/workflows/release.yml, tools/release-gate.sh, tests/test_release.py
- **Commit:** `82ce34cb6df433c9bb9bc4712171eae488f55a3d`

## T-011 (sprint 0)
- **Description:** Write the README
- **Intent:** [INT-0001](../intents/INT-0001-the-cruor-framework.md)
- **Completed:** 2026-11-23T19:11:44Z
- **Files modified:** README.md, tests/test_readme.py
- **Commit:** `8c8938c4e036c3178c607b5363ed70054ee08676`

## T-012 (sprint 0)
- **Description:** Bundle in CI on every push and keep the result
- **Intent:** [INT-0005](../intents/INT-0005-versioned-releases.md)
- **Completed:** 2026-11-23T19:13:03Z
- **Files modified:** .github/workflows/ci.yml, tests/test_ci.py
- **Commit:** `88a7f9fb39fd7cb3739d3190ddf223580806c6eb`

## T-216 (sprint 1)
- **Description:** Begin the record of the review that keeps the repository in its own terms, with its first entry
- **Intent:** [INT-0001](../intents/INT-0001-the-cruor-framework.md)
- **Completed:** 2026-11-24T05:10:00Z
- **Files modified:** docs/sprints/s1/sprint-tests/own-terms-review.md
- **Commit:** `b44d52904b02e5b46601f996d12123c4fab9decb`

## T-215 (sprint 1)
- **Description:** Confirm what the default branch holds and mark the fonts intent realized; this takes up and closes backlog task T-103
- **Intent:** [INT-0002](../intents/INT-0002-cruor-web-fonts.md), [INT-0001](../intents/INT-0001-the-cruor-framework.md)
- **Completed:** 2026-11-24T05:14:00Z
- **Files modified:** docs/intents/INT-0002-cruor-web-fonts.md, docs/intents/INT-0001-the-cruor-framework.md
- **Commit:** `2155159ec8b3d62c1e6fd462c4979270f18d00f9`

## T-201 (sprint 1)
- **Description:** Write the look down as look/theme.toml, write up its form, and give the tool a look command that reads and judges it
- **Intent:** [INT-0004](../intents/INT-0004-the-look-as-a-theme-file.md)
- **Completed:** 2026-11-24T05:12:58Z
- **Files modified:** look/theme.toml, look/THEME.md, src/theme.rs, src/main.rs, tests/theme.rs, tests/common/mod.rs, tests/test_theme_form.py, docs/intents/INT-0004-the-look-as-a-theme-file.md
- **Commit:** `4bdab55debb3354129c997fbb2fda6ab90eb8bfb`

## T-202 (sprint 1)
- **Description:** Have look write look/tokens.css from the theme file, and look --check and check hold the two together
- **Intent:** [INT-0004](../intents/INT-0004-the-look-as-a-theme-file.md)
- **Completed:** 2026-11-24T05:15:08Z
- **Files modified:** src/look.rs, src/main.rs, src/theme.rs, look/tokens.css, tests/look.rs, tests/cli.rs, tests/theme.rs
- **Commit:** `9129a8159b59b0a6eaef19271060611422e8c2c7`

## T-203 (sprint 1)
- **Description:** Test, from the theme file, the contrast it promises: entries in the theme file, a check in the tool that names the pair that fails, and a check that no rule sets a pair the file has not promised
- **Intent:** [INT-0003](../intents/INT-0003-cruentous-atonement-look.md), [INT-0004](../intents/INT-0004-the-look-as-a-theme-file.md)
- **Completed:** 2026-11-24T05:18:04Z
- **Files modified:** src/contrast.rs, src/theme.rs, src/look.rs, src/main.rs, look/theme.toml, look/THEME.md, tests/contrast.rs, tests/stylesheets.py, tests/test_promised_pairs.py, tests/test_theme_form.py, docs/intents/INT-0003-cruentous-atonement-look.md
- **Commit:** `f31bc3d9b8093c94b26aa10c6a5a325bb200207f`

## T-211 (sprint 1)
- **Description:** Make the means of checking a page in a browser: open it with script on or off and stillness asked for, and measure contrast from a picture of what is drawn
- **Intent:** [INT-0006](../intents/INT-0006-the-furniture.md), [INT-0003](../intents/INT-0003-cruentous-atonement-look.md)
- **Completed:** 2026-11-24T05:22:30Z
- **Files modified:** tests/browser.py, tests/test_browser_means.py, docs/intents/INT-0006-the-furniture.md
- **Commit:** `59a231490fffc213cb0aea35b1102b76bc8c3a1b`

## T-204 (sprint 1)
- **Description:** Lay the look's ground in look/cruentous-atonement.css: the stone, the candle and the dark at the edges, with every bound on the stone held against the stone as drawn
- **Intent:** [INT-0003](../intents/INT-0003-cruentous-atonement-look.md), [INT-0004](../intents/INT-0004-the-look-as-a-theme-file.md)
- **Completed:** 2026-11-24T05:25:43Z
- **Files modified:** look/cruentous-atonement.css, tests/test_look_css.py, tests/test_look_ground.py, tests/pages/bare.html
- **Commit:** `03ddacb29f8f89a002711018dafeac2d656102f1`

## T-205 (sprint 1)
- **Description:** Dress plain HTML in the look: the inscription, carved headings driven by the theme file, the seal, links, lists, quotations, the sigil, code and tables, with stillness when asked and plain letters in print
- **Intent:** [INT-0003](../intents/INT-0003-cruentous-atonement-look.md), [INT-0004](../intents/INT-0004-the-look-as-a-theme-file.md)
- **Completed:** 2026-11-24T05:30:41Z
- **Files modified:** look/cruentous-atonement.css, tests/test_look_page.py, tests/test_look_css.py, tests/pages/plain.html
- **Commit:** PENDING

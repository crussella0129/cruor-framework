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

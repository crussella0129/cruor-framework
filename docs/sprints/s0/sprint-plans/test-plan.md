Finalized - DO NOT EDIT

# Sprint 0 Test Plan

Rust tests are named as plain identifiers; Python tests begin `test_`;
checks made by a person or read from a CI run begin `review_` or `ci_`.
Each task's tests are written with the task and land in its commit.

## Intent Traceability
| Intent | Acceptance criterion | Build task / EARS clause | Verification |
|--------|----------------------|--------------------------|--------------|
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 1: thirty-two `.woff2`, named by family and style | T-003 / WHEN `fonts/` is listed THEN it SHALL hold exactly thirty-two `.woff2` files | `test_fonts_are_the_thirty_two` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 1 | T-003 / WHEN `families.toml` is read THEN it SHALL list the eight families | `test_families_list_has_eight` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 2: the licence beside the fonts, with the copyright line | T-003 / WHEN `OFL.txt` is read THEN it SHALL hold the licence beneath the copyright line | `test_ofl_text_and_copyright_line` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 2: the README says the fonts are under it | T-011 / WHEN the README is read THEN it SHALL say that the fonts are offered under… | `test_readme_states_terms` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 3: one stylesheet, four styles joined | T-004 / WHEN `css` is run THEN thirty-two rules with the right descriptors | `css_has_thirty_two_rules`, `css_rule_descriptors_match_style` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 3 | T-004 / WHEN `fonts.css` is read THEN its opening comment SHALL say both sets of terms | `css_comment_states_both_terms` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 3 | T-004 / WHEN the stylesheet differs THEN `css --check` SHALL exit non-zero | `css_check_fails_when_stale` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 3 | T-004 / WHEN a listed font is missing THEN `css` SHALL exit non-zero | `css_fails_on_missing_font` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 3 | T-004 / WHEN `css` is run twice THEN byte-identical | `css_is_deterministic` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 3: asking for a bold or an italic gives that file; 4: a browser loads each face and sets text in it | T-007 / WHEN the specimen is opened over HTTP THEN one line in each face, a different `.woff2` fetched for each | `test_specimen_loads_all_faces`, `test_specimen_fetches_a_file_for_each_face`, `test_specimen_styles_of_a_family_differ`, `test_specimen_is_not_in_a_fallback` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 4 | T-007 / WHEN the specimen is read THEN no script, every address a bare name in `fonts/` | `test_specimen_is_self_contained` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5: the manifest, and a check that fails | T-005 / WHEN `manifest --source-commit` is run with a full id THEN commit, name, size, SHA-256 | `manifest_records_every_font` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5 | T-005 / WHEN the commit is malformed, or none is given and none recorded THEN exit non-zero, nothing written | `manifest_refuses_short_commit`, `manifest_refuses_when_no_commit_known` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5 | T-005 / WHEN a font's bytes differ THEN `manifest --check` SHALL exit non-zero | `manifest_check_fails_on_changed_byte` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5 | T-005 / WHEN a font is missing or unlisted THEN `manifest --check` SHALL exit non-zero | `manifest_check_fails_on_missing_font`, `manifest_check_fails_on_unlisted_font` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5 | T-005 / WHEN `manifest` is run without a commit and one is recorded THEN it SHALL keep it | `manifest_keeps_source_commit` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5 | T-005 / WHEN `check` is run THEN both checks | `check_runs_both`, `repository_passes_check` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5: a font's own name against its rule | T-006 / WHEN every font agrees THEN exit 0 | `test_check_fonts_passes_on_repository` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5 | T-006 / WHEN any font disagrees THEN exit non-zero, naming file and field | `test_check_fonts_fails_on_swapped_fonts`, `test_check_fonts_fails_on_wrong_weight_in_rule` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5 | T-006 / WHEN the guards are run THEN they SHALL also run `check_fonts.py` | `test_guards_run_check_fonts` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5: something runs the checks | T-001 / WHEN `--help` is run THEN it SHALL name the commands | `help_names_the_commands` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5 | T-001 / WHEN `run-guards.sh` is run THEN every check, failing if any fails | `test_guards_run_every_check`, `test_guards_fail_when_any_check_fails` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5 | T-001 / WHEN a commit is pushed THEN CI SHALL run the guards | `test_ci_workflow_runs_guards`, `ci_guards_green_on_dev` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5 | T-001 / WHEN the repository is checked out THEN line feeds, and fonts unchanged | `test_gitattributes_fixes_line_ends`, `test_tracked_text_has_no_carriage_returns` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 5: the first tag is the crate's version | T-001 / WHEN `Cargo.toml` is read THEN the version SHALL be `0.1.0` | `test_crate_version_is_first_release` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 6: no other file from the Cruor project | T-003 / WHEN tracked files are listed THEN the only font files SHALL be those thirty-two | `test_no_other_font_files_tracked` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 6, for files of any kind | T-013 / WHEN a review is made THEN it SHALL list the files each commit adds or changes and compare them with its task | `review_commits_touch_only_their_tasks` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) | 5: which build of Cruor the files came from; 6 | T-013 / WHEN the review covers the commit that takes the fonts in THEN the commit id, the clean tree, and the inventory compared | `review_intake_matches_inventory` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 1: one command puts a release together | T-008 / WHEN `bundle --out` is run THEN the folder SHALL hold the files, the archive and its checksum | `bundle_holds_expected_files`, `bundle_archive_holds_same_files`, `bundle_archive_checksum_is_right` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 1 | T-008 / WHEN `manifest.json` is read THEN version, commit, and each file's name, size, SHA-256 | `bundle_manifest_matches_files` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 1 | T-008 / WHEN a check would fail THEN `bundle` SHALL write nothing | `bundle_refuses_when_a_check_fails` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 1 | T-008 / WHEN the folder is not empty THEN `bundle` SHALL write nothing | `bundle_refuses_nonempty_folder` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 2: the same commit, the same manifest | T-008 / WHEN `bundle` is run twice THEN byte-identical | `bundle_is_reproducible` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 2, across machines | T-012 / WHEN a commit is pushed THEN CI SHALL run `bundle` and keep its folder | `test_ci_workflow_keeps_bundle`, `ci_bundle_matches_local` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 2 | T-012 / WHEN `ci.yml` is read THEN no leave to write | `test_ci_workflow_cannot_write` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 3: relative addresses | T-008 / WHEN the bundle's stylesheet is read THEN every address SHALL be a bare file name present | `bundle_css_addresses_are_bare_and_present` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 4: a build that fetches and checks ends with identical files | T-009 / WHEN the example is run against a served bundle THEN every file fetched and checked | `test_fetch_release_matches_repository` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 4 | T-009 / WHEN a fetched file disagrees THEN exit non-zero, no copy left | `test_fetch_release_fails_on_tampered_file` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 4 | T-009 / WHEN the manifest lists a name that is not bare THEN exit non-zero before fetching | `test_fetch_release_rejects_path_in_name` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 4 | T-009 / WHEN `--manifest-sha256` does not match THEN exit non-zero before fetching | `test_fetch_release_honours_pinned_manifest` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 4 | T-009 / WHEN the address cannot be reached THEN exit non-zero | `test_fetch_release_fails_when_unreachable` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 5: a pushed tag on `main` publishes, whole or not at all | T-008 / WHEN the tag is not the crate's version THEN `bundle` SHALL write nothing | `bundle_refuses_mismatched_tag`, `bundle_accepts_matching_tag` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 5 | T-010 / WHEN a tag beginning `v` is pushed THEN guards, bundle, publish | `test_release_workflow_runs_guards_then_bundle_then_publish` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 5 | T-010 / WHEN the commit is not on `main`, or the release exists, or a step fails THEN publish nothing | `test_release_workflow_calls_gate`, `test_release_workflow_has_no_continue_on_error` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 5 | T-010 / WHEN `release-gate.sh` is run THEN exit 0 only on `main` with no release for the tag | `test_release_gate_passes_on_main`, `test_release_gate_refuses_off_main`, `test_release_gate_refuses_existing_release`, `test_release_gate_names_leftover_draft` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 5 | T-010 / WHEN it publishes THEN draft, add every file, then public | `test_release_workflow_publishes_from_draft` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 5: the release proves itself | T-010 / WHEN the release is public THEN it SHALL run the fetch example against its own address | `test_release_workflow_checks_itself`; `release_checks_itself_v0_1_0` (not yet possible, see below) |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 5 | T-010 / WHEN that check fails THEN the release SHALL return to a draft before the workflow fails | `test_release_workflow_withdraws_on_failed_check` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 6: the README gives the address pattern and shows the fetch | T-011 / WHEN the README is read THEN the address pattern, the fetch, the pinned manifest | `test_readme_gives_release_address`, `test_readme_shows_fetch_example` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 1: the Book and a README that says what the kit is | T-011 / WHEN the README is read THEN what the kit is, the look named and not in yet | `test_readme_says_what_the_kit_is` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 1 | T-011 / WHEN the README is read THEN the eight families and four styles | `test_readme_lists_eight_families` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 1 | T-011 / WHEN the README is read THEN a page linking `fonts.css` | `test_readme_shows_linking_page` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 1 | T-011 / WHEN the README is read THEN bold and italic by weight and style; "Regular" part of the name | `test_readme_explains_weight_and_style` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 1 | T-011 / WHEN the README is read THEN what running the checks requires | `test_readme_states_check_requirements` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 1 | T-011 / WHEN each path and command the README names is looked up THEN it SHALL exist | `test_readme_names_existing_paths_and_commands`, `review_readme_against_checklist` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 3: both licences at the root | T-002 / WHEN the root is listed THEN `LICENSE-MIT` and `LICENSE-APACHE` | `test_code_licences_present` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 3 | T-002 / WHEN `Cargo.toml` is read THEN `MIT OR Apache-2.0` | `test_crate_declares_licence` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 3: the README says which terms cover what | T-011 / WHEN the README is read THEN the terms and the three licence files | `test_readme_states_terms` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 5: nothing in the repository or its history names another typeface | T-013 / WHEN commits are about to be pushed THEN a review SHALL search every changed file and message, and read the new prose | `review_own_terms_before_each_push` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 5 | T-013 / WHEN the commits include font files THEN their name tables, and their metadata and private blocks, SHALL be read and searched | `review_font_name_tables` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 5 | T-013 / WHEN a pull request, tag or release is about to be made THEN its text SHALL be searched first | `review_pull_request_text` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 5 | T-013 / WHEN a pull request arrives that the owner did not write THEN it SHALL be searched and read before it is merged | `review_updater_pull_requests` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 5 | T-013 / WHEN a review is made THEN the record SHALL gain an entry, the number found none | `review_record_is_complete` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 5 | T-013 / WHEN something is found THEN rewrite before pushing, or stop for the owner | `review_record_is_complete` (each entry says what was done with anything found) |

## Unit Tests

### T-001 unit tests
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)
- `help_names_the_commands`: `--help` exits 0 and its text holds `css`, `manifest`, `check` and `bundle`.
- `test_guards_run_every_check`: `tools/run-guards.sh` holds each of the six commands of T-001's clause.
- `test_guards_fail_when_any_check_fails`: run once for each command the script runs. A folder of stand-ins for every one of them (`cargo`, `ruff`, `pytest`, `python`) is put first on the path; all exit 0 but the one under test, which exits 1. The script exits non-zero each time, and exits 0 when all stand-ins exit 0. No real check runs, so the test cannot call itself.
- `test_ci_workflow_runs_guards`: `ci.yml` is triggered by pushes to `main` and `dev` and by pull requests; it sets up the pinned toolchain, Python with `tools/requirements.txt`, the browser and Node 20; and a step runs `tools/run-guards.sh`.
- `test_gitattributes_fixes_line_ends`: `.gitattributes` sets text files to line feeds and marks `*.woff2` binary.
- `test_tracked_text_has_no_carriage_returns`: no tracked text file, as git stores it, holds a carriage return.
- `test_crate_version_is_first_release`: `Cargo.toml`'s version is `0.1.0`.

### T-002 unit tests
- **Intent:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)
- `test_code_licences_present`: both files exist; `LICENSE-MIT` holds "Permission is hereby granted" and the copyright line; `LICENSE-APACHE` holds "Apache License" and "Version 2.0".
- `test_crate_declares_licence`: `Cargo.toml`'s `license` is `MIT OR Apache-2.0`.

### T-003 unit tests
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)
- `test_fonts_are_the_thirty_two`: the `.woff2` files in `fonts/` are exactly the eight stems by the four styles.
- `test_families_list_has_eight`: `families.toml` parses to eight families, each with a name, a stem and a kind that is one of the three, and the stems are the eight of T-003's clause.
- `test_ofl_text_and_copyright_line`: `OFL.txt` begins with the copyright line exactly as INT-0002 criterion 2 gives it, and holds "SIL OPEN FONT LICENSE Version 1.1" and the licence's five conditions.
- `test_no_other_font_files_tracked`: of the files `git ls-files` gives, those ending `.woff2`, `.woff`, `.ttf` or `.otf` are exactly the thirty-two.

### T-004 unit tests
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)
- `css_has_thirty_two_rules`: the text `css` makes from the list holds thirty-two `@font-face` rules, no two alike.
- `css_rule_descriptors_match_style`: for each family and style, the rule's family, weight, slant, file and `font-display` are as T-004 gives them.
- `css_comment_states_both_terms`: the opening comment holds `MIT OR Apache-2.0` for the file and "SIL Open Font License" for the fonts, and says the file is made by the tool.
- `css_check_fails_when_stale`: in a temporary copy with one character of `fonts.css` changed, `css --check` exits non-zero, names the file and leaves it as it was.
- `css_fails_on_missing_font`: in a temporary copy with one font removed, `css` and `css --check` exit non-zero and name it.
- `css_is_deterministic`: two runs give the same bytes, and no carriage return is among them.

### T-005 unit tests
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)
- `manifest_records_every_font`: after `manifest --source-commit` with a forty-character id in a temporary copy, the manifest holds that id and thirty-two entries whose sizes and SHA-256 are those of the files.
- `manifest_refuses_short_commit`: `--source-commit abc1234` → non-zero, nothing written.
- `manifest_refuses_when_no_commit_known`: no manifest, no `--source-commit` → non-zero, nothing written.
- `manifest_check_fails_on_changed_byte`: one byte of one font changed → non-zero, the file named.
- `manifest_check_fails_on_missing_font`: one font removed → non-zero, the file named.
- `manifest_check_fails_on_unlisted_font`: a `.woff2` the list does not call for added → non-zero, the file named.
- `manifest_keeps_source_commit`: `manifest` with no commit given leaves the recorded commit as it was.
- `check_runs_both`: `check` fails when only the stylesheet is stale, and fails when only the manifest is.

### T-006 unit tests
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)
- `test_check_fonts_passes_on_repository`: exit 0 on `fonts/`.
- `test_check_fonts_fails_on_swapped_fonts`: in a copy where a Bold and an Italic of one family have changed places, exit non-zero, naming a swapped file and the field.
- `test_check_fonts_fails_on_wrong_weight_in_rule`: in a copy whose `fonts.css` gives one Bold the weight 400, exit non-zero, naming the file and `weight`.
- `test_guards_run_check_fonts`: `tools/run-guards.sh` runs `tools/check_fonts.py` on `fonts/`; and with the stand-ins of `test_guards_fail_when_any_check_fails`, a failing stand-in for it makes the script exit non-zero.

### T-007 unit tests
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)
- `test_specimen_is_self_contained`: `specimen.html` is parsed; it holds no `script` element and no event-handler attribute; every `href`, every `src` and every `url(...)` in it is a bare file name, with no slash, no scheme and no parent path, that names a file in `fonts/`.

### T-008 unit tests
- **Intent:** [INT-0005](../../../intents/INT-0005-versioned-releases.md)
- `bundle_holds_expected_files`: the folder holds exactly the thirty-two fonts, `fonts.css`, `OFL.txt`, `LICENSE-MIT`, `LICENSE-APACHE`, `manifest.json`, the archive named for the crate's version and its `.sha256` file, and no folder.
- `bundle_archive_holds_same_files`: the archive's entries are the fonts, `fonts.css`, `OFL.txt`, the two licences and `manifest.json`, each with the same bytes as the file beside the archive.
- `bundle_archive_checksum_is_right`: the `.sha256` file gives the SHA-256 of the archive beside it.
- `bundle_manifest_matches_files`: `manifest.json` gives the crate's version and the recorded commit, lists the fonts, `fonts.css`, `OFL.txt` and the two licences and nothing else, and each size and SHA-256 is that of the file.
- `bundle_is_reproducible`: two runs into two folders give byte-identical `manifest.json`, archive and checksum file.
- `bundle_refuses_when_a_check_fails`: with a stale stylesheet, and again with a changed font, `bundle` exits non-zero and the folder is absent or empty.
- `bundle_refuses_nonempty_folder`: a folder holding one file → non-zero, the file untouched, nothing added.
- `bundle_css_addresses_are_bare_and_present`: every `url(...)` in the bundle's `fonts.css` has no slash and names a file in the folder.
- `bundle_refuses_mismatched_tag`: `--tag v9.9.9` → non-zero, nothing written.
- `bundle_accepts_matching_tag`: `--tag v<the crate's version>` → the bundle is written.

### T-010 unit tests
- **Intent:** [INT-0005](../../../intents/INT-0005-versioned-releases.md)
- The first group reads `release.yml` as data; the second runs `tools/release-gate.sh` for real. None of them publishes anything.
- `test_release_workflow_runs_guards_then_bundle_then_publish`: the workflow is triggered only by pushed tags beginning `v`; its steps run the guards, then `bundle` with the pushed tag, then the publishing, in that order; it alone among the workflows asks for leave to write contents.
- `test_release_workflow_calls_gate`: a step before the bundling and the publishing runs `tools/release-gate.sh` with the pushed tag, on a checkout that has the whole history of `main`.
- `test_release_workflow_has_no_continue_on_error`: no step is set to continue on error, and the publishing steps come after every check.
- `test_release_workflow_publishes_from_draft`: the release is created as a draft with the bundle's files, and a later step makes it public.
- `test_release_workflow_checks_itself`: after the release is made public, a step runs `examples/fetch-release.mjs` against the release's download address with `--manifest-sha256` set from the bundle the workflow built.
- `test_release_workflow_withdraws_on_failed_check`: a step that runs only if that check failed returns the release to a draft, and the workflow still ends as failed.
- `test_release_gate_passes_on_main`: in a scratch repository with a tag on a commit of `origin/main`, and a stand-in for the GitHub client that reports no release, the gate exits 0.
- `test_release_gate_refuses_off_main`: the same with the tag on a commit that is on another branch only → non-zero, saying the commit is not on `main`.
- `test_release_gate_refuses_existing_release`: the stand-in reports a public release for the tag → non-zero, saying so.
- `test_release_gate_names_leftover_draft`: the stand-in reports a draft for the tag → non-zero, naming the draft as one to remove.

### T-011 unit tests
- **Intent:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)
- `test_readme_says_what_the_kit_is`: the README names the Cruor framework and Cruentous Atonement and says the look is not in the kit yet.
- `test_readme_lists_eight_families`: each of the eight family names is in the README, and the four styles.
- `test_readme_shows_linking_page`: a code block of the README holds a `link` to `fonts.css` and a `font-family` naming one of the eight families.
- `test_readme_explains_weight_and_style`: the README names `font-weight` and `font-style` in a sentence about bold and italic, and says of a family whose name ends in "Regular" that the word is part of the name.
- `test_readme_gives_release_address`: the README holds the address pattern of T-011's clause.
- `test_readme_shows_fetch_example`: the README shows `examples/fetch-release.mjs` being run with an address and a folder, and with `--manifest-sha256`.
- `test_readme_states_check_requirements`: the README names `rust-toolchain.toml`, `tools/requirements.txt`, Playwright's browser and Node 20.
- `test_readme_states_terms`: the README names the SIL Open Font License 1.1 and the reserved name for the fonts, says `fonts/OFL.txt` states the fonts' terms, names `MIT OR Apache-2.0` for the code, and names the three licence files.
- `test_readme_names_existing_paths_and_commands`: every repository path the README gives in code marks exists, and every tool command it shows is one `--help` names.

### T-012 unit tests
- **Intent:** [INT-0005](../../../intents/INT-0005-versioned-releases.md)
- `test_ci_workflow_keeps_bundle`: `ci.yml` runs `bundle` after the guards and uploads its folder as an artefact.
- `test_ci_workflow_cannot_write`: `ci.yml` grants read access to contents and nothing more.

## Integration Tests

### The repository as it stands
- **Intents:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md), [INT-0005](../../../intents/INT-0005-versioned-releases.md)
- `repository_passes_check`: `check` exits 0 on the tracked files (T-003, T-004 and T-005 composed: the fonts taken in, the stylesheet and the manifest all agree).
- `ci_guards_green_on_dev`: the CI run for the sprint's last commit on `dev` passed `tools/run-guards.sh`; the run's address and the commit are recorded in the test report.
- `ci_bundle_matches_local`: the `manifest.json` in that run's artefact is byte-identical to one made by `bundle` on the owner's machine at the same commit. This is the proof that a checkout on another system gives the same bytes.

### The reviews of T-013
- **Intents:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md), [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)
- Each is made by a person or an agent working from outside the repository, and each is proven by an entry in `docs/sprints/s0/sprint-tests/own-terms-review.md`.
- `review_own_terms_before_each_push`: for every push of the sprint there is an entry, made before it, whose range of commits begins where the last entry ended; the search covered the content of every file each commit adds or changes and every commit message, against the list kept outside the repository; the new prose was read once for comparisons. A commit whose only change is a new entry is covered by that entry. Pass: every commit on `dev` at the time of the Test phase falls in some entry's range or is such a commit, and every entry's number found is none.
- `review_font_name_tables`: the entry covering T-003's commit says that every name-table string of all thirty-two fonts was read with fontTools and searched, and that each font's WOFF2 metadata block and private block was read too or is absent. Pass: number found none.
- `review_pull_request_text`: an entry covers the title and body of the sprint's pull request, made before it is opened. It is made at the Loop phase, after the Test phase has read the record, and is read there before the pull request is opened. Pass: number found none.
- `review_updater_pull_requests`: every pull request open against the repository that the owner did not write has an entry giving its number and what was found in its title, body and commits. Pass: none found in any that is merged; any in which something was found is closed.
- `review_commits_touch_only_their_tasks`: each entry lists the files every covered commit adds or changes and sets them against the Touches of the commit's task; the Book's ledgers and records are accounted for as such. Pass: nothing unaccounted for, and no file from the Cruor project other than the thirty-two fonts.
- `review_intake_matches_inventory`: the entry covering T-003's commit gives the full commit id of Cruor that was built, says the build's tree had nothing uncommitted, and sets the thirty-two files' glyph counts and family names against `font-inventory.md`, recording every difference. Pass: the id is the one in `fonts/manifest.toml`, and any difference is explained.
- `review_record_is_complete`: at the Test phase the whole record is read. Pass: no push made so far lacks an entry, and each entry says what was done with anything found. The entries for the pushes that close the sprint and open its pull request are outside what the Test phase can judge; they are added and read at the Loop phase.

### The README, read
- **Intent:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)
- `review_readme_against_checklist`: the README is read once with this list, each item marked in the test report: every command shown was run as written and did what the README says; the example page, saved beside `fonts.css` and opened, shows its text in the family it names; the address pattern, filled in with a file name the bundle holds, has the form GitHub documents; nothing is said of the look beyond its name and that it is to come.

## End-to-End Tests
- **Status:** possible
- `test_specimen_loads_all_faces`: `fonts/` is served over HTTP on the local machine; a headless Chromium opens `specimen.html`; each of the thirty-two faces, asked for by family, weight and style, reports as loaded; no request failed and none left the local address. Pass: thirty-two loaded, no failure.
- `test_specimen_fetches_a_file_for_each_face`: for each of the thirty-two faces in turn, a fresh page that links `fonts.css` and sets no text asks for that face alone through the browser's font-loading interface, by family, weight and style; the requests are watched. Pass: each time exactly one `.woff2` is fetched, and it is the file that family and style call for.
- `test_specimen_styles_of_a_family_differ`: for Cruor Lite Regular and for Cruor Lite Mono, pictures are taken of the four sample sentences alone, without their labels (Regular, Bold, Italic, Bold Italic, the same sentence); no two of a family's four are the same picture. Pass: all differ, in both families. The test above is what shows the difference comes from the right file and not from the browser's own imitation of a bold or an italic.
- `test_specimen_is_not_in_a_fallback`: the same sentence set in Cruor Sans Regular and in the browser's own fallback font measures two different widths. Pass: they differ.
- `test_fetch_release_matches_repository`: `bundle` writes a folder; it is served over HTTP on the local machine; `node examples/fetch-release.mjs <address> <empty folder>` exits 0; every font, `fonts.css` and `OFL.txt` in that folder is byte-identical to the file in `fonts/`, and `LICENSE-MIT` and `LICENSE-APACHE` to the files at the repository's root. Pass: exit 0 and all identical.
- `test_fetch_release_fails_on_tampered_file`: the same, with one byte of one served font changed after the bundle is written. Pass: non-zero exit, the file named, no copy of it in the folder.
- `test_fetch_release_rejects_path_in_name`: a served `manifest.json` lists a name holding a parent path. Pass: non-zero exit, and nothing written outside or inside the folder.
- `test_fetch_release_honours_pinned_manifest`: run with the right `--manifest-sha256`, exit 0; with a wrong one, non-zero exit and no file fetched.
- `test_fetch_release_fails_when_unreachable`: the example run against a local address nothing listens on. Pass: non-zero exit, the address named.

One end-to-end proof cannot be made in this sprint:

- `release_checks_itself_v0_1_0` — **not yet possible.** It is the release workflow's own last step, run for real: the files of `v0.1.0` fetched from `https://github.com/crussella0129/cruor-framework/releases/download/v0.1.0/` and checked against the pinned manifest. Unlocked by: the owner's word to push the tag after this sprint's pull request is merged. It is queued as backlog task T-102 under [INT-0005](../../../intents/INT-0005-versioned-releases.md), to be recorded by the sprint in progress when the tag is pushed (the next sprint, which builds the look, if not before). INT-0005 is not `realized` until that run has passed. Until then criterion 5 rests on the tests of `release.yml`, the four tests that run its gate for real, the two tag tests, and the bundle CI makes on every push.

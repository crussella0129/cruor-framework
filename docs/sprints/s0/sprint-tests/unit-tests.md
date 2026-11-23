# Sprint 0 Unit Test Results

- **Tested commit:** `49dd8934f7f04f721504e7cbd0ef2c1d45209ccf`, the head of `dev` when the run was made, with nothing uncommitted.
- **Runner:** `bash tools/run-guards.sh`, the repository's one guard script,
  run in a fresh clone of `dev` on the owner's machine (Windows 11, Rust 1.99.1, Python 3.13.11,
  Node 24.12.0, Chromium as Playwright 1.58.0 installs it) with
  `PYTEST_ADDOPTS=-v` set, so that every test is named in the output. The
  script exited 0.
- **The same commit in CI:** run [45266754572](https://github.com/crussella0129/cruor-framework/actions/runs/45266754572) on Ubuntu 24.04,
  with Python 3.13 and Node 20, conclusion `success`. CI runs the same
  script.
- **What the script confirmed, step by step:** `cargo fmt --check` passed;
  `cargo clippy --all-targets -- -D warnings` passed; `cargo test`,
  32 passed and 0 failed; `ruff format --check` passed;
  `ruff check` passed; `python -I tools/check_fonts.py fonts` passed;
  `pytest`, 91 passed and none failed.

Every unit test the test plan names ran and passed. Each row is one named
test; the test plan says what each asserts.

## T-001 unit tests
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)

| Test | Where it is | Result |
|---|---|---|
| `help_names_the_commands` | `tests/cli.rs` | passed |
| `test_guards_run_every_check` | `tests/test_guards.py` | passed |
| `test_guards_fail_when_any_check_fails` | `tests/test_guards.py` | 7 cases, all passed |
| `test_ci_workflow_runs_guards` | `tests/test_ci.py` | passed |
| `test_gitattributes_fixes_line_ends` | `tests/test_repository.py` | passed |
| `test_tracked_text_has_no_carriage_returns` | `tests/test_repository.py` | passed |
| `test_crate_version_is_first_release` | `tests/test_repository.py` | passed |

## T-002 unit tests
- **Intent:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)

| Test | Where it is | Result |
|---|---|---|
| `test_code_licences_present` | `tests/test_licences.py` | passed |
| `test_crate_declares_licence` | `tests/test_licences.py` | passed |

## T-003 unit tests
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)

| Test | Where it is | Result |
|---|---|---|
| `test_fonts_are_the_thirty_two` | `tests/test_fonts_intake.py` | passed |
| `test_families_list_has_eight` | `tests/test_fonts_intake.py` | passed |
| `test_ofl_text_and_copyright_line` | `tests/test_fonts_intake.py` | passed |
| `test_no_other_font_files_tracked` | `tests/test_fonts_intake.py` | passed |

## T-004 unit tests
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)

| Test | Where it is | Result |
|---|---|---|
| `css_has_thirty_two_rules` | `src/css.rs` | passed |
| `css_rule_descriptors_match_style` | `src/css.rs` | passed |
| `css_comment_states_both_terms` | `src/css.rs` | passed |
| `css_check_fails_when_stale` | `tests/css.rs` | passed |
| `css_fails_on_missing_font` | `tests/css.rs` | passed |
| `css_is_deterministic` | `tests/css.rs` | passed |

## T-005 unit tests
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)

| Test | Where it is | Result |
|---|---|---|
| `manifest_records_every_font` | `tests/manifest.rs` | passed |
| `manifest_refuses_short_commit` | `tests/manifest.rs` | passed |
| `manifest_refuses_when_no_commit_known` | `tests/manifest.rs` | passed |
| `manifest_check_fails_on_changed_byte` | `tests/manifest.rs` | passed |
| `manifest_check_fails_on_missing_font` | `tests/manifest.rs` | passed |
| `manifest_check_fails_on_unlisted_font` | `tests/manifest.rs` | passed |
| `manifest_keeps_source_commit` | `tests/manifest.rs` | passed |
| `check_runs_both` | `tests/manifest.rs` | passed |

## T-006 unit tests
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)

| Test | Where it is | Result |
|---|---|---|
| `test_check_fonts_passes_on_repository` | `tests/test_check_fonts.py` | passed |
| `test_check_fonts_fails_on_swapped_fonts` | `tests/test_check_fonts.py` | passed |
| `test_check_fonts_fails_on_wrong_weight_in_rule` | `tests/test_check_fonts.py` | passed |
| `test_guards_run_check_fonts` | `tests/test_check_fonts.py` | passed |

## T-007 unit tests
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md)

| Test | Where it is | Result |
|---|---|---|
| `test_specimen_is_self_contained` | `tests/test_specimen.py` | passed |

## T-008 unit tests
- **Intent:** [INT-0005](../../../intents/INT-0005-versioned-releases.md)

| Test | Where it is | Result |
|---|---|---|
| `bundle_holds_expected_files` | `tests/bundle.rs` | passed |
| `bundle_archive_holds_same_files` | `tests/bundle.rs` | passed |
| `bundle_archive_checksum_is_right` | `tests/bundle.rs` | passed |
| `bundle_manifest_matches_files` | `tests/bundle.rs` | passed |
| `bundle_is_reproducible` | `tests/bundle.rs` | passed |
| `bundle_refuses_when_a_check_fails` | `tests/bundle.rs` | passed |
| `bundle_refuses_nonempty_folder` | `tests/bundle.rs` | passed |
| `bundle_css_addresses_are_bare_and_present` | `tests/bundle.rs` | passed |
| `bundle_refuses_mismatched_tag` | `tests/bundle.rs` | passed |
| `bundle_accepts_matching_tag` | `tests/bundle.rs` | passed |

## T-010 unit tests
- **Intent:** [INT-0005](../../../intents/INT-0005-versioned-releases.md)

| Test | Where it is | Result |
|---|---|---|
| `test_release_workflow_runs_guards_then_bundle_then_publish` | `tests/test_release.py` | passed |
| `test_release_workflow_calls_gate` | `tests/test_release.py` | passed |
| `test_release_workflow_has_no_continue_on_error` | `tests/test_release.py` | passed |
| `test_release_workflow_publishes_from_draft` | `tests/test_release.py` | passed |
| `test_release_workflow_checks_itself` | `tests/test_release.py` | passed |
| `test_release_workflow_withdraws_on_failed_check` | `tests/test_release.py` | passed |
| `test_release_gate_passes_on_main` | `tests/test_release.py` | passed |
| `test_release_gate_refuses_off_main` | `tests/test_release.py` | passed |
| `test_release_gate_refuses_existing_release` | `tests/test_release.py` | passed |
| `test_release_gate_names_leftover_draft` | `tests/test_release.py` | passed |

## T-011 unit tests
- **Intent:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)

| Test | Where it is | Result |
|---|---|---|
| `test_readme_says_what_the_kit_is` | `tests/test_readme.py` | passed |
| `test_readme_lists_eight_families` | `tests/test_readme.py` | passed |
| `test_readme_shows_linking_page` | `tests/test_readme.py` | passed |
| `test_readme_explains_weight_and_style` | `tests/test_readme.py` | passed |
| `test_readme_gives_release_address` | `tests/test_readme.py` | passed |
| `test_readme_shows_fetch_example` | `tests/test_readme.py` | passed |
| `test_readme_states_check_requirements` | `tests/test_readme.py` | passed |
| `test_readme_states_terms` | `tests/test_readme.py` | passed |
| `test_readme_names_existing_paths_and_commands` | `tests/test_readme.py` | passed |

## T-012 unit tests
- **Intent:** [INT-0005](../../../intents/INT-0005-versioned-releases.md)

| Test | Where it is | Result |
|---|---|---|
| `test_ci_workflow_keeps_bundle` | `tests/test_ci.py` | passed |
| `test_ci_workflow_cannot_write` | `tests/test_ci.py` | passed |

## Tests beyond the plan

These ran in the same script and passed. The plan does not name them.
Some were written with their tasks, to hold a part the named tests lean
on; the others were added in the Test phase, where its first critique
([critique-round-1.md](critique-round-1.md)) found a clause held loosely.

Five tests the plan names were tightened in the Test phase too, and
pass as tightened:

- `test_tracked_text_has_no_carriage_returns` (first critique, C-006):
  the search must end as git's "none found".
- `test_ofl_text_and_copyright_line` (first critique, C-007): the
  licence's text beneath the copyright line is held by its SHA-256.
- `test_release_gate_passes_on_main` (first critique, C-003): the
  question the gate asks the GitHub client is held whole.
- `test_release_workflow_runs_guards_then_bundle_then_publish` and
  `test_ci_workflow_runs_guards` (second critique,
  [critique-round-2.md](critique-round-2.md), C-003): the guard and bundle
  commands are held whole, and CI may not carry on after an error.

| Test | Where it is | Written | Result |
|---|---|---|---|
| `a_checksum_is_the_known_one` | `src/manifest.rs` | with its task, in the Build | passed |
| `a_commit_id_is_forty_hexadecimal_characters` | `src/manifest.rs` | with its task, in the Build | passed |
| `a_list_gives_four_files_a_family` | `src/families.rs` | with its task, in the Build | passed |
| `a_list_is_refused_for_what_would_break_a_rule_or_a_file_name` | `src/families.rs` | with its task, in the Build | passed |
| `bundle_carries_the_repository_files_unchanged` | `tests/bundle.rs` | with its task, in the Build | passed |
| `css_writes_what_the_repository_holds` | `tests/css.rs` | with its task, in the Build | passed |
| `test_check_fonts_fails_on_fonts_swapped_across_families` | `tests/test_check_fonts.py` | in the Test phase, for C-001 of the first critique | passed |
| `test_check_fonts_fails_on_wrong_family_in_rule` | `tests/test_check_fonts.py` | in the Test phase, for C-001 of the first critique | passed |
| `test_readme_says_of_the_look_only_its_name` | `tests/test_readme.py` | in the Test phase, for C-002 of the first critique | passed |
| `test_release_gate_asks_for_every_release` | `tests/test_release.py` | in the Test phase, for C-003 of the first critique | passed |
| `test_release_gate_refuses_a_tag_that_is_not_there` | `tests/test_release.py` | with its task, in the Build | passed |

## Counts

- Named in the plan as unit tests: 63 tests, 63 passed, 0 failed.
- Beyond the plan: 11 tests, 11 passed, 0 failed.
- The script's own totals: `cargo test` 32 passed; `pytest` 91
  passed. Those totals also hold the integration and end-to-end tests,
  which have their own records beside this one, and count each case of a
  test that runs once for each of several inputs.

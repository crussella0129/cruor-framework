# Sprint 0 End-to-End Test Results

- **Status:** possible, and run.
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

Each of these drives the thing itself: a headless Chromium opening the
specimen page over HTTP on this machine, or Node running the fetch example
against a bundle served over HTTP on this machine. No request leaves the
machine.

- **Intents:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) (the specimen), [INT-0005](../../../intents/INT-0005-versioned-releases.md) (the fetch)

| Test | Where it is | Result |
|---|---|---|
| `test_specimen_loads_all_faces` | `tests/test_specimen.py` | passed |
| `test_specimen_fetches_a_file_for_each_face` | `tests/test_specimen.py` | 32 cases, all passed |
| `test_specimen_styles_of_a_family_differ` | `tests/test_specimen.py` | 2 cases, all passed |
| `test_specimen_is_not_in_a_fallback` | `tests/test_specimen.py` | passed |
| `test_fetch_release_matches_repository` | `tests/test_fetch_release.py` | passed |
| `test_fetch_release_fails_on_tampered_file` | `tests/test_fetch_release.py` | passed |
| `test_fetch_release_rejects_path_in_name` | `tests/test_fetch_release.py` | passed |
| `test_fetch_release_honours_pinned_manifest` | `tests/test_fetch_release.py` | passed |
| `test_fetch_release_fails_when_unreachable` | `tests/test_fetch_release.py` | passed |

`test_specimen_fetches_a_file_for_each_face` runs once for each of the
thirty-two faces; `test_specimen_styles_of_a_family_differ` once for each
of two families.

## Beyond the plan

A release's own address answers each file with a redirect to another
address. The plan left that to the first real release; the Test phase's
first critique (C-005) pointed out that it can be met on this machine, with
a second local address that redirects to the first.

| Test | Where it is | Written | Result |
|---|---|---|---|
| `test_fetch_release_follows_a_redirect` | `tests/test_fetch_release.py` | in the Test phase, for C-005 of the first critique | passed |

## Counts

- End-to-end tests the plan names as possible: 9 tests, 9 passed, 0 failed.
- Beyond the plan: 1 test, 1 passed, 0 failed.

## Not yet possible

- `release_checks_itself_v0_1_0`: not run, as the test plan says. It is
  the release workflow's own last step, run for real against the public
  address of `v0.1.0`. No tag has been pushed and no release exists.
  Unlocked by the owner's word to push the tag after this sprint's pull
  request is merged; queued as backlog task T-102 under [INT-0005](../../../intents/INT-0005-versioned-releases.md).
  Until then that intent's criterion 5 rests on the tests of
  `release.yml`, the tests that run `tools/release-gate.sh` for real, the
  two tag tests of `bundle`, and the bundle CI makes on every push.
  A redirect is now met locally (above); what remains for that run is
  GitHub's own address and the files as GitHub serves them.

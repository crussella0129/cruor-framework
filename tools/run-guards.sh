#!/usr/bin/env bash
# Every check the repository has, in one place and in one order. CI runs
# exactly this script, so a change that passes here passes there.
#
#   bash tools/run-guards.sh
set -u
cd "$(dirname "$0")/.."

# step <name> <command...>: say which step starts, run it, and stop the whole
# run with the step's own exit code if it fails.
step() {
  local name=$1
  shift
  printf '\n==> %s\n' "$name"
  "$@" || {
    local status=$?
    printf '\n==> FAILED: %s (exit %s)\n' "$name" "$status" >&2
    exit "$status"
  }
}

step "The tool is formatted" cargo fmt --check
step "The tool has no lints" cargo clippy --all-targets -- -D warnings
step "The tool's tests" cargo test
step "The checks are formatted" ruff format --check
step "The checks have no lints" ruff check
step "Each font agrees with its rule" python -I tools/check_fonts.py fonts
step "The checks' tests" pytest

printf '\n==> Every check passed\n'

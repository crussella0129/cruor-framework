#!/usr/bin/env bash
# May this tag be released?
#
#   bash tools/release-gate.sh <tag>
#
# Run from the repository's root. It exits 0 only if both of these hold:
#
#   - the commit the tag names is on main (an ancestor of origin/main), and
#   - no release exists for the tag, whether public or a draft.
#
# Otherwise it says which, and exits 1. A draft left behind by an earlier
# run is named as such: it is the owner's to remove, and nothing here
# removes it.
#
# It reads the repository's releases with the GitHub client, `gh`, which
# takes the repository from GH_REPO or from the checkout's own remote.
set -u

tag=${1:-}
if [ -z "$tag" ] || [ "$#" -ne 1 ]; then
  echo "usage: bash tools/release-gate.sh <tag>" >&2
  exit 2
fi

fail() {
  printf 'release-gate: %s\n' "$*" >&2
  exit 1
}

commit=$(git rev-parse --quiet --verify "refs/tags/$tag^{commit}") ||
  fail "there is no tag $tag in this checkout"

git rev-parse --quiet --verify "refs/remotes/origin/main^{commit}" >/dev/null ||
  fail "origin/main is not known in this checkout; the gate needs the whole history of main"

git merge-base --is-ancestor "$commit" refs/remotes/origin/main ||
  fail "the commit that $tag names is not on main; only a tagged commit on main is released"

# Every release of the repository, drafts among them, one to a line: its
# tag, a tab, and whether it is a draft.
releases=$(gh api --paginate 'repos/{owner}/{repo}/releases' \
  --jq '.[] | "\(.tag_name)\t\(.draft)"') ||
  fail "the repository's releases could not be listed"

while IFS=$'\t' read -r name draft; do
  [ "$name" = "$tag" ] || continue
  if [ "$draft" = true ]; then
    fail "a draft release for $tag was left behind by an earlier run; it is the owner's to remove before the tag is tried again"
  fi
  fail "a release for $tag already exists; a release is never published over another"
done <<<"$releases"

printf 'release-gate: %s is on main and has no release; it may be released\n' "$tag"

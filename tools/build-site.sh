#!/usr/bin/env bash
# Put the showroom's site together in a folder, as it is served on the web.
#
#   bash tools/build-site.sh <folder>
#
# The folder ends up holding the showroom and what it links, each where the
# repository keeps it, so that every address in the showroom's page means on
# the web what it means in a copy of the repository:
#
#   showroom/   the showroom
#   fonts/      the fonts and their stylesheet
#   look/       the look's stylesheets
#   index.html  a page that sends a visitor to showroom/
#
# Nothing is made here that the repository does not hold, but that one page.
# The folder must be absent or empty: a site is put together in a folder of
# its own.
set -u

out=${1:-}
if [ -z "$out" ] || [ "$#" -ne 1 ]; then
  echo "usage: bash tools/build-site.sh <folder>" >&2
  exit 2
fi

fail() {
  printf 'build-site: %s\n' "$*" >&2
  exit 1
}

root=$(cd "$(dirname "$0")/.." && pwd) || fail "cannot find the repository"

if [ -e "$out" ]; then
  [ -d "$out" ] || fail "$out is not a folder"
  [ -z "$(ls -A "$out")" ] || fail "$out is not empty; a site is put together in a folder of its own"
fi
mkdir -p "$out" || fail "cannot make $out"

for folder in showroom fonts look; do
  [ -d "$root/$folder" ] || fail "the repository has no $folder/"
  cp -R "$root/$folder" "$out/$folder" || fail "cannot copy $folder/"
done

cat > "$out/index.html" <<'PAGE' || fail "cannot write index.html"
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The Cruor framework: the showroom</title>
<meta http-equiv="refresh" content="0; url=showroom/">
<link rel="canonical" href="showroom/">
</head>
<body>
<p><a href="showroom/">The showroom of the Cruor framework</a></p>
</body>
</html>
PAGE

printf 'build-site: the site is in %s\n' "$out"

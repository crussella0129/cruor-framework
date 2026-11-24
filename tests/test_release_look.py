"""The look in a release: a page beside a release's files, opened in a browser.

A release is one flat set of files. A page set among them links the four
stylesheets by bare name and sets the look's class, and that is all it does.
"""

import shutil
import subprocess

import pytest

import browser
from helpers import ROOT, serve

LOOK = browser.theme()

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>A page beside a release</title>
<link rel="stylesheet" href="fonts.css">
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="cruentous-atonement.css">
<link rel="stylesheet" href="furniture.css">
</head>
<body class="cruentous-atonement">
<h1 id="title">A page beside a release</h1>
<h2 id="heading">It takes the look on</h2>
<p id="text">It links four stylesheets by bare name, and sets one class.</p>
<pre><code id="code">let blood = shed(1504);</code></pre>
<button type="button" class="cruor-button" id="part">Atone</button>
</body>
</html>
"""


@pytest.fixture(scope="module")
def engine():
    with browser.chromium() as found:
        yield found


@pytest.fixture(scope="module")
def release(tmp_path_factory):
    """A release as `bundle` puts it together, with one page set in it."""
    made = tmp_path_factory.mktemp("release") / "bundle"
    subprocess.run(
        ["cargo", "run", "--quiet", "--", "bundle", "--out", str(made)],
        cwd=ROOT,
        check=True,
    )
    folder = shutil.copytree(made, tmp_path_factory.mktemp("served") / "release")
    assert not [path for path in folder.iterdir() if path.is_dir()]
    (folder / "page.html").write_text(PAGE, encoding="utf-8", newline="\n")
    return folder


def test_release_look_works_flat(engine, release):
    asked, failed = [], []
    with serve(release) as (address, _):
        context = engine.new_context(viewport=browser.WINDOW, reduced_motion="reduce")
        page = context.new_page()
        page.on("request", lambda request: asked.append(request.url))
        page.on("requestfailed", lambda request: failed.append(request.url))
        try:
            page.goto(address + "page.html")
            page.wait_for_load_state("networkidle")
            page.evaluate("document.fonts.ready.then(() => true)")
            faces = page.evaluate(
                "[...document.fonts].map(face =>"
                " [face.family.replaceAll('\"', ''), face.status])"
            )
            set_in = page.evaluate(
                """() => Object.fromEntries(['title', 'heading', 'text', 'code']
                    .map(id => [id, getComputedStyle(document.getElementById(id))
                        .fontFamily.split(',')[0].trim().replaceAll('"', '')]))"""
            )
            ground = page.evaluate("getComputedStyle(document.body).backgroundColor")
            stone = page.evaluate(
                "getComputedStyle(document.body, '::before').backgroundImage"
            )
            part = page.evaluate(
                "getComputedStyle(document.getElementById('part')).borderTopColor"
            )
        finally:
            context.close()

    # Everything asked for was in the release's own folder, and was had.
    assert failed == []
    assert asked and all(url.startswith(address) for url in asked), asked
    names = {url.removeprefix(address) for url in asked}
    assert all("/" not in name for name in names), names
    assert all((release / name).is_file() for name in names), names

    # Every face the page uses loaded: the four the look names, each from a
    # file of the release.
    assert not [face for face in faces if face[1] == "error"]
    loaded = {face[0] for face in faces if face[1] == "loaded"}
    for role in ("title", "heading", "text", "code"):
        assert set_in[role] == LOOK["font"][role], role
        assert LOOK["font"][role] in loaded, role
    assert [name for name in names if name.endswith(".woff2")]

    # The page's ground is the look's: the theme file's colour, with the
    # stone drawn over it; and a part is dressed.
    assert browser.colour(ground) == browser.colour(LOOK["colour"]["page"])
    assert stone.startswith('url("data:image/svg+xml,')
    assert browser.colour(part) != browser.colour("rgb(0, 0, 0)")

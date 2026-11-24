"""Publishing the showroom: the site put together for real, and the workflow
read as data.

Nothing here publishes anything. The script that makes the site is run into
a temporary folder, and the showroom is opened from that folder as it would
be from the web.
"""

import subprocess
from html.parser import HTMLParser

import pytest

import browser
from helpers import ROOT, find_bash, read_workflow, serve

SCRIPT = ROOT / "tools" / "build-site.sh"
CARRIED = ["showroom", "fonts", "look"]
LOOK = browser.theme()


def build(folder) -> subprocess.CompletedProcess:
    return subprocess.run(
        [find_bash(), SCRIPT.as_posix(), folder.as_posix()],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    folder = tmp_path_factory.mktemp("site") / "site"
    result = build(folder)
    assert result.returncode == 0, result.stderr
    return folder


def files_under(folder) -> dict[str, bytes]:
    return {
        path.relative_to(folder).as_posix(): path.read_bytes()
        for path in sorted(folder.rglob("*"))
        if path.is_file()
    }


class Read(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.sends = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.tags.append(tag)
        if tag == "meta" and attributes.get("http-equiv") == "refresh":
            self.sends.append(attributes.get("content"))
        if tag == "a":
            self.links.append(attributes.get("href"))


def test_site_is_built_whole(site, tmp_path):
    made = files_under(site)
    expected = {"index.html": made.get("index.html")}
    for folder in CARRIED:
        for name, content in files_under(ROOT / folder).items():
            expected[f"{folder}/{name}"] = content
    # The three folders as the repository holds them, one page, and no more.
    assert sorted(made) == sorted(expected)
    assert made == expected
    assert "showroom/index.html" in made and "fonts/fonts.css" in made
    assert "look/tokens.css" in made

    # The one page it makes sends a visitor to the showroom, with no script,
    # and offers a link for a browser that does not follow.
    page = Read()
    page.feed(made["index.html"].decode("utf-8"))
    assert page.sends == ["0; url=showroom/"]
    assert page.links == ["showroom/"]
    assert "script" not in page.tags and "style" not in page.tags

    # A site is put together in a folder of its own.
    again = build(site)
    assert again.returncode != 0 and "not empty" in again.stderr
    assert files_under(site) == made
    fresh = tmp_path / "does" / "not" / "exist"
    assert build(fresh).returncode == 0
    assert files_under(fresh) == made


def test_showroom_loads_from_the_site(site):
    asked, failed, statuses = [], [], {}
    with browser.chromium() as engine, serve(site) as (address, _):
        context = engine.new_context(viewport=browser.WINDOW, reduced_motion="reduce")
        page = context.new_page()
        page.on("request", lambda request: asked.append(request.url))
        page.on("requestfailed", lambda request: failed.append(request.url))
        page.on("response", lambda got: statuses.update({got.url: got.status}))
        try:
            # A visitor comes to the site's head and is sent to the showroom.
            page.goto(address)
            page.wait_for_url(address + "showroom/")
            page.wait_for_load_state("networkidle")
            page.evaluate("document.fonts.ready.then(() => true)")
            faces = page.evaluate(
                "[...document.fonts].map(face =>"
                " [face.family.replaceAll('\"', ''), face.status])"
            )
            pictures = page.evaluate(
                "[...document.images].map(img => img.complete && img.naturalWidth > 0)"
            )
            ground = page.evaluate("getComputedStyle(document.body).backgroundColor")
        finally:
            context.close()
    assert failed == []
    assert all(url.startswith(address) for url in asked), asked
    assert all(status == 200 for status in statuses.values()), statuses
    assert not [face for face in faces if face[1] == "error"]
    loaded = {face[0] for face in faces if face[1] == "loaded"}
    for role in ("title", "heading", "text", "code"):
        assert LOOK["font"][role] in loaded, role
    assert pictures and all(pictures)
    assert browser.colour(ground) == browser.colour(LOOK["colour"]["page"])


def test_pages_workflow_publishes_the_site():
    workflow = read_workflow("pages.yml")
    # On a push to the default branch, and by hand.
    assert workflow["on"] == {"push": {"branches": ["main"]}, "workflow_dispatch": None}

    jobs = workflow["jobs"]
    assert list(jobs) == ["guards", "publish"]
    guards, publish = jobs["guards"], jobs["publish"]

    # The guards run first, whole, and nothing forgives their failure.
    assert [
        step["run"] for step in guards["steps"] if "Guards" in step.get("name", "")
    ] == ["bash tools/run-guards.sh"]
    assert publish["needs"] == "guards"
    for job in jobs.values():
        assert "continue-on-error" not in job
        for step in job["steps"]:
            assert "continue-on-error" not in step

    # It publishes only when the owner has said so, by the variable.
    assert publish["if"] == "vars.SHOWROOM == 'published'"
    assert "if" not in guards
    assert not [step for step in publish["steps"] if "if" in step]

    # What it publishes is what the repository's own script makes.
    steps = publish["steps"]
    used = [step.get("uses", "").split("@")[0] for step in steps]
    build = [index for index, step in enumerate(steps) if "run" in step]
    assert [steps[index]["run"] for index in build] == ["bash tools/build-site.sh site"]
    upload = used.index("actions/upload-pages-artifact")
    deploy = used.index("actions/deploy-pages")
    assert used.index("actions/checkout") < build[0] < upload < deploy
    assert steps[upload]["with"] == {"path": "site"}
    assert publish["environment"]["name"] == "github-pages"

    # Exactly three permissions, and no other, anywhere in it: the workflow
    # itself may only read, and the job that publishes holds the three.
    assert workflow["permissions"] == {"contents": "read"}
    assert "permissions" not in guards
    assert publish["permissions"] == {
        "contents": "read",
        "pages": "write",
        "id-token": "write",
    }

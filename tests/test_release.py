"""Publishing a release: the workflow read as data, and its gate run for real.

Nothing here publishes anything. The gate is run against a scratch
repository, with a stand-in for the GitHub client that reports whichever
releases a test names.
"""

import os
import subprocess

import pytest

from helpers import ROOT, find_bash, read_workflow, steps_of

GATE = ROOT / "tools" / "release-gate.sh"
WORKFLOWS = ROOT / ".github" / "workflows"


def release_steps() -> list[dict]:
    return steps_of(read_workflow("release.yml"))


def index_of(steps: list[dict], text: str) -> int:
    """Where the one step whose command holds a text is."""
    found = [index for index, step in enumerate(steps) if text in step.get("run", "")]
    assert len(found) == 1, f"one step runs {text!r}: {found}"
    return found[0]


def test_release_workflow_runs_guards_then_bundle_then_publish():
    workflow = read_workflow("release.yml")
    assert workflow["on"] == {"push": {"tags": ["v*"]}}

    steps = steps_of(workflow)
    guards = index_of(steps, "bash tools/run-guards.sh")
    bundle = index_of(steps, "bundle --out dist")
    publish = index_of(steps, "gh release create")
    assert guards < bundle < publish
    # Each command whole: nothing after it that would forgive a failure.
    assert steps[guards]["run"] == "bash tools/run-guards.sh"
    assert (
        steps[bundle]["run"] == 'cargo run --release -- bundle --out dist --tag "$TAG"'
    )
    assert 'gh release create "$TAG" dist/*' in " ".join(steps[publish]["run"].split())
    assert workflow["jobs"]["release"]["env"]["TAG"] == "${{ github.ref_name }}"


def test_only_release_and_pages_may_write():
    # Two workflows ask for leave to write, each for the one thing it does:
    # the release's for a release, and the showroom's to publish a site. No
    # workflow may write as a whole, and no other asks at all.
    may_write = {
        "release.yml": [{"contents": "write"}],
        "pages.yml": [{"contents": "read", "pages": "write", "id-token": "write"}],
    }
    found = sorted(path.name for path in WORKFLOWS.glob("*.yml"))
    assert set(may_write) <= set(found)
    for name in found:
        other = read_workflow(name)
        assert other["permissions"] == {"contents": "read"}, name
        grants = [job.get("permissions", {}) for job in other["jobs"].values()]
        writes = [grant for grant in grants if "write" in str(grant)]
        assert writes == may_write.get(name, []), name


def test_release_notes_tell_of_the_look():
    # What a release says of itself names what it holds: the fonts, and the
    # look with its theme file.
    steps = release_steps()
    notes = steps[index_of(steps, "gh release create")]["run"]
    assert "--notes" in notes
    said = notes.split("--notes", 1)[1]
    for told in ("web fonts", "Cruentous Atonement", "stylesheets", "theme file"):
        assert told in said, told


def test_release_workflow_calls_gate():
    steps = release_steps()
    gate = index_of(steps, "tools/release-gate.sh")
    assert steps[gate]["run"] == 'bash tools/release-gate.sh "$TAG"'
    assert gate < index_of(steps, "bash tools/run-guards.sh")
    assert gate < index_of(steps, "bundle --out dist")
    assert gate < index_of(steps, "gh release create")

    # The gate needs the whole history of main.
    checkout = steps[0]
    assert checkout["uses"].startswith("actions/checkout@")
    assert checkout["with"]["fetch-depth"] == 0


def test_release_workflow_has_no_continue_on_error():
    workflow = read_workflow("release.yml")
    for job in workflow["jobs"].values():
        assert "continue-on-error" not in job
    steps = steps_of(workflow)
    for step in steps:
        assert "continue-on-error" not in step, step
    # Every check comes before anything is published, and none is optional.
    publish = index_of(steps, "gh release create")
    for step in steps[:publish]:
        assert "if" not in step, step


def test_release_workflow_publishes_from_draft():
    steps = release_steps()
    create = index_of(steps, "gh release create")
    public = index_of(steps, "--draft=false")
    assert "--draft" in steps[create]["run"].split()
    assert "--verify-tag" in steps[create]["run"].split()
    assert create < public
    assert steps[public]["run"] == 'gh release edit "$TAG" --draft=false'


def test_release_workflow_checks_itself():
    steps = release_steps()
    public = index_of(steps, "--draft=false")
    proof = index_of(steps, "examples/fetch-release.mjs")
    assert public < proof
    command = steps[proof]["run"]
    assert 'address="https://github.com/$GH_REPO/releases/download/$TAG/"' in command
    assert "manifest_sha256=$(sha256sum dist/manifest.json" in command
    assert '--manifest-sha256 "$manifest_sha256"' in command
    # If no attempt passes, the step fails.
    assert command.rstrip().endswith("exit 1")


def test_release_workflow_withdraws_on_failed_check():
    steps = release_steps()
    proof = index_of(steps, "examples/fetch-release.mjs")
    withdraw = index_of(steps, "--draft=true")
    assert steps[proof]["id"] == "proof"
    assert proof < withdraw == len(steps) - 1
    # It runs only when the proof failed, and running it does not turn a
    # failed run into a passed one: `failure()` leaves the run failed.
    assert steps[withdraw]["if"] == "failure() && steps.proof.conclusion == 'failure'"
    assert 'gh release edit "$TAG" --draft=true' in steps[withdraw]["run"]
    assert "left for the owner" in steps[withdraw]["run"]


STAND_IN_GH = """#!/usr/bin/env bash
# A stand-in for the GitHub client. It notes what it was asked, one argument
# to a line, and reports the releases the test names, one to a line: a tag,
# a tab, and whether it is a draft.
printf '%s\\n' "$@" >> "$STAND_IN_CALLS"
printf '%s' "$STAND_IN_RELEASES"
"""

# What the gate must ask the GitHub client: every release of the repository,
# drafts among them and however many pages they fill, each as its tag, a tab
# and whether it is a draft. The stand-in answers in that shape whatever it
# is asked, so the question itself is held here.
THE_QUESTION = [
    "api",
    "--paginate",
    "repos/{owner}/{repo}/releases",
    "--jq",
    r'.[] | "\(.tag_name)\t\(.draft)"',
]


def git(folder, *arguments: str) -> str:
    identity = {
        "GIT_AUTHOR_NAME": "A test",
        "GIT_AUTHOR_EMAIL": "test@example.invalid",
        "GIT_COMMITTER_NAME": "A test",
        "GIT_COMMITTER_EMAIL": "test@example.invalid",
    }
    return subprocess.run(
        ["git", "-c", "core.hooksPath=", "-c", "commit.gpgsign=false", *arguments],
        cwd=folder,
        env={**os.environ, **identity},
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


@pytest.fixture
def checkout(tmp_path):
    """A scratch checkout: one commit on main, and one more on a branch.

    Gives the checkout and the two commits.
    """
    origin = tmp_path / "origin"
    origin.mkdir()
    git(origin, "init", "--quiet", "--initial-branch=main")
    (origin / "file.txt").write_text("one\n", encoding="utf-8")
    git(origin, "add", "file.txt")
    git(origin, "commit", "--quiet", "-m", "one")

    clone = tmp_path / "clone"
    git(tmp_path, "clone", "--quiet", str(origin), str(clone))
    on_main = git(clone, "rev-parse", "HEAD")
    git(clone, "switch", "--quiet", "-c", "work")
    (clone / "file.txt").write_text("two\n", encoding="utf-8")
    git(clone, "commit", "--quiet", "-am", "two")
    off_main = git(clone, "rev-parse", "HEAD")
    return clone, on_main, off_main


def run_gate(
    checkout, tmp_path, tag: str, releases: str
) -> subprocess.CompletedProcess:
    stand_ins = tmp_path / "stand-ins"
    stand_ins.mkdir(exist_ok=True)
    (stand_ins / "gh").write_text(STAND_IN_GH, encoding="utf-8", newline="\n")
    (stand_ins / "gh").chmod(0o755)
    environment = dict(os.environ)
    environment["PATH"] = str(stand_ins) + os.pathsep + environment["PATH"]
    environment["STAND_IN_RELEASES"] = releases
    environment["STAND_IN_CALLS"] = (tmp_path / "asked-of-gh.txt").as_posix()
    return subprocess.run(
        [find_bash(), str(GATE), tag],
        cwd=checkout,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def asked_of_gh(tmp_path) -> list[str]:
    """Every argument the gate gave the stand-in, in order."""
    noted = tmp_path / "asked-of-gh.txt"
    return noted.read_text(encoding="utf-8").splitlines() if noted.exists() else []


def test_release_gate_passes_on_main(checkout, tmp_path):
    clone, on_main, _ = checkout
    git(clone, "tag", "v0.1.0", on_main)
    # Other releases exist; none is for this tag.
    result = run_gate(clone, tmp_path, "v0.1.0", "v0.0.9\tfalse\nv0.1.0-rc.1\ttrue\n")
    assert result.returncode == 0, result.stderr
    assert "may be released" in result.stdout
    assert asked_of_gh(tmp_path) == THE_QUESTION


def test_release_gate_asks_for_every_release(checkout, tmp_path):
    clone, on_main, _ = checkout
    git(clone, "tag", "v0.1.0", on_main)
    for releases in ["", "v0.1.0\tfalse\n", "v0.1.0\ttrue\n"]:
        (tmp_path / "asked-of-gh.txt").unlink(missing_ok=True)
        run_gate(clone, tmp_path, "v0.1.0", releases)
        # Asked once, and for every release: no filter that could hide a draft.
        assert asked_of_gh(tmp_path) == THE_QUESTION


def test_release_gate_refuses_off_main(checkout, tmp_path):
    clone, _, off_main = checkout
    git(clone, "tag", "v0.1.0", off_main)
    result = run_gate(clone, tmp_path, "v0.1.0", "")
    assert result.returncode != 0
    assert "not on main" in result.stderr


def test_release_gate_refuses_existing_release(checkout, tmp_path):
    clone, on_main, _ = checkout
    git(clone, "tag", "v0.1.0", on_main)
    result = run_gate(clone, tmp_path, "v0.1.0", "v0.1.0\tfalse\n")
    assert result.returncode != 0
    assert "a release for v0.1.0 already exists" in result.stderr


def test_release_gate_names_leftover_draft(checkout, tmp_path):
    clone, on_main, _ = checkout
    git(clone, "tag", "v0.1.0", on_main)
    result = run_gate(clone, tmp_path, "v0.1.0", "v0.0.9\tfalse\nv0.1.0\ttrue\n")
    assert result.returncode != 0
    assert "a draft release for v0.1.0 was left behind" in result.stderr
    assert "the owner's to remove" in result.stderr


def test_release_gate_refuses_a_tag_that_is_not_there(checkout, tmp_path):
    clone, _, _ = checkout
    result = run_gate(clone, tmp_path, "v0.1.0", "")
    assert result.returncode != 0
    assert "there is no tag v0.1.0" in result.stderr

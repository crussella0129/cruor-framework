"""A build fetching a release and checking it, end to end.

The tool puts a release together, the folder is served over HTTP on this
machine alone, and the worked example fetches it as a page's build would.
"""

import hashlib
import json
import shutil
import socket
import subprocess

import pytest

from helpers import ROOT, redirect_to, serve

EXAMPLE = ROOT / "examples" / "fetch-release.mjs"
# The look: its theme file, the tokens made from it, its two stylesheets.
LOOK = ["theme.toml", "tokens.css", "cruentous-atonement.css", "furniture.css"]


@pytest.fixture(scope="module")
def bundle(tmp_path_factory):
    """A release, as `bundle` puts it together from the repository."""
    out = tmp_path_factory.mktemp("release") / "bundle"
    subprocess.run(
        ["cargo", "run", "--quiet", "--", "bundle", "--out", str(out)],
        cwd=ROOT,
        check=True,
    )
    return out


def fetch(address: str, folder, *more: str) -> subprocess.CompletedProcess:
    node = shutil.which("node")
    assert node, "the fetch example needs Node 20 or newer"
    return subprocess.run(
        [node, str(EXAMPLE), address, str(folder), *more],
        capture_output=True,
        text=True,
        check=False,
    )


def files_in(folder) -> dict[str, bytes]:
    return {path.name: path.read_bytes() for path in folder.iterdir()}


def test_fetch_release_matches_repository(bundle, tmp_path):
    fetched = tmp_path / "fetched"
    with serve(bundle) as (address, _asked):
        result = fetch(address, fetched)
    assert result.returncode == 0, result.stderr

    got = files_in(fetched)
    manifest = json.loads(got["manifest.json"])
    assert sorted(got) == sorted(
        [file["name"] for file in manifest["files"]] + ["manifest.json"]
    )
    assert len(got) == 41

    fonts = sorted(path.name for path in (ROOT / "fonts").glob("*.woff2"))
    assert len(fonts) == 32
    for name in [*fonts, "fonts.css", "OFL.txt"]:
        assert got[name] == (ROOT / "fonts" / name).read_bytes(), name
    for name in ["LICENSE-MIT", "LICENSE-APACHE"]:
        assert got[name] == (ROOT / name).read_bytes(), name
    for name in LOOK:
        assert got[name] == (ROOT / "look" / name).read_bytes(), name


def test_fetch_release_follows_a_redirect(bundle, tmp_path):
    # A release's own address answers each file with a redirect to another.
    fetched = tmp_path / "fetched"
    with serve(bundle) as (address, asked), redirect_to(address) as first_address:
        result = fetch(first_address, fetched)
    assert result.returncode == 0, result.stderr

    got = files_in(fetched)
    assert len(got) == 41
    for name, content in got.items():
        assert content == (bundle / name).read_bytes(), name
    # Every file was had by way of the redirect, from the address behind it.
    assert sorted(asked) == sorted(f"/{name}" for name in got)


def test_fetch_release_fails_on_tampered_file(bundle, tmp_path):
    served = shutil.copytree(bundle, tmp_path / "served")
    spoiled = served / "CruorThornamentalMono-Regular.woff2"
    changed = bytearray(spoiled.read_bytes())
    changed[100] ^= 1
    spoiled.write_bytes(bytes(changed))

    fetched = tmp_path / "fetched"
    with serve(served) as (address, _asked):
        result = fetch(address, fetched)
    assert result.returncode != 0
    assert "CruorThornamentalMono-Regular.woff2" in result.stderr
    assert not (fetched / "CruorThornamentalMono-Regular.woff2").exists()


def test_fetch_release_rejects_path_in_name(bundle, tmp_path):
    served = shutil.copytree(bundle, tmp_path / "site" / "served")
    (tmp_path / "site" / "escaped.txt").write_text("outside\n", encoding="utf-8")
    manifest = json.loads((served / "manifest.json").read_text(encoding="utf-8"))
    manifest["files"].append({"name": "../escaped.txt", "size": 8, "sha256": "0" * 64})
    (served / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    fetched = tmp_path / "work" / "fetched"
    with serve(tmp_path / "site") as (address, asked):
        result = fetch(address + "served/", fetched)
    assert result.returncode != 0
    assert "not a bare file name" in result.stderr
    # It stopped at the manifest: no file was fetched, and nothing was written.
    assert asked == ["/served/manifest.json"]
    assert not fetched.exists()
    assert not (tmp_path / "work" / "escaped.txt").exists()


def test_fetch_release_honours_pinned_manifest(bundle, tmp_path):
    right = hashlib.sha256((bundle / "manifest.json").read_bytes()).hexdigest()
    wrong = hashlib.sha256(b"another manifest").hexdigest()

    with serve(bundle) as (address, asked):
        result = fetch(address, tmp_path / "pinned", "--manifest-sha256", right)
        assert result.returncode == 0, result.stderr
        assert len(files_in(tmp_path / "pinned")) == 41

        asked.clear()
        result = fetch(address, tmp_path / "refused", "--manifest-sha256", wrong)
    assert result.returncode != 0
    assert "manifest.json is not the one expected" in result.stderr
    assert asked == ["/manifest.json"]
    assert not (tmp_path / "refused").exists()


def test_fetch_release_fails_when_unreachable(tmp_path):
    # A port of this machine that nothing listens on.
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    address = f"http://127.0.0.1:{port}/"

    result = fetch(address, tmp_path / "fetched")
    assert result.returncode != 0
    assert address in result.stderr
    assert not (tmp_path / "fetched").exists()

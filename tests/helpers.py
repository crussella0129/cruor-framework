"""What the Python tests share: where the repository is, and how to run things."""

import os
import pathlib
import shutil
import subprocess

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def find_bash() -> str:
    """The path of a bash that sees this machine's own tools.

    On Windows that is Git Bash. The `bash` in System32 is another system's
    shell, which sees none of the machine's tools, so it is passed over.
    """
    candidates = [shutil.which("bash")]
    git = shutil.which("git")
    if git:
        # Git for Windows keeps its bash two folders above git.exe.
        candidates.append(
            str(pathlib.Path(git).resolve().parent.parent / "bin" / "bash.exe")
        )
    for candidate in candidates:
        if not candidate or not pathlib.Path(candidate).exists():
            continue
        try:
            system = subprocess.run(
                [candidate, "-c", "uname -s"],
                capture_output=True,
                text=True,
                check=False,
            ).stdout.strip()
        except OSError:
            continue
        if os.name != "nt" and system:
            return candidate
        if system.startswith(("MINGW", "MSYS")):
            return candidate
    raise RuntimeError("no usable bash was found; on Windows the tests need Git Bash")


def tracked_files() -> list[str]:
    """Every path git tracks, as git gives it."""
    listing = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
    ).stdout
    return [name for name in listing.decode("utf-8").split("\0") if name]


def read_workflow(name: str) -> dict:
    """A workflow of the repository, read as data.

    YAML reads the bare word `on` as the truth value, so the triggers are put
    back under the key a person would look for.
    """
    workflow = yaml.safe_load(
        (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
    )
    if True in workflow:
        workflow["on"] = workflow.pop(True)
    return workflow


def steps_of(workflow: dict) -> list[dict]:
    """Every step of every job of a workflow, in order."""
    return [step for job in workflow["jobs"].values() for step in job["steps"]]


def commands_of(workflow: dict) -> str:
    """Every shell command a workflow runs, as one text."""
    return "\n".join(step.get("run", "") for step in steps_of(workflow))

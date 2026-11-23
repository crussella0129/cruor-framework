"""The CI workflow, read as data: what starts it and what it runs."""

from helpers import commands_of, read_workflow, steps_of


def test_ci_workflow_runs_guards():
    workflow = read_workflow("ci.yml")

    triggers = workflow["on"]
    assert sorted(triggers["push"]["branches"]) == ["dev", "main"]
    assert "pull_request" in triggers

    commands = commands_of(workflow)
    uses = {
        step["uses"].split("@")[0]: step
        for step in steps_of(workflow)
        if "uses" in step
    }

    # The toolchain rust-toolchain.toml pins.
    assert "rustup toolchain install" in commands
    # Python, with the checks' packages at their pinned versions.
    assert "actions/setup-python" in uses
    assert "pip install -r tools/requirements.txt" in commands
    # The browser the checks drive.
    assert "playwright install" in commands
    assert "chromium" in commands
    # The oldest Node the fetch example promises to run on.
    assert uses["actions/setup-node"]["with"]["node-version"] == 20

    assert "bash tools/run-guards.sh" in commands

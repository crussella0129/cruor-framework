//! The tool as a person meets it: by its commands.

use std::process::Command;

/// The path of the built tool.
fn tool() -> Command {
    Command::new(env!("CARGO_BIN_EXE_cruor-framework"))
}

#[test]
fn help_names_the_commands() {
    let output = tool().arg("--help").output().expect("the tool runs");
    assert!(output.status.success(), "--help exits 0");
    let help = String::from_utf8(output.stdout).expect("help is text");
    for command in ["css", "manifest", "look", "check", "bundle"] {
        assert!(
            help.lines()
                .any(|line| line.trim_start().starts_with(command)),
            "--help names `{command}`:\n{help}"
        );
    }
}

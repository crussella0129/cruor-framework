//! What the tests of the tool share: the tool itself, and a copy of the
//! repository's files to spoil without harm.

#![allow(dead_code)]

use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};

use tempfile::TempDir;

/// The repository's root.
pub fn repository() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
}

/// The built tool, pointed at a root.
pub fn tool(root: &Path) -> Command {
    let mut command = Command::new(env!("CARGO_BIN_EXE_cruor-framework"));
    command.arg("--root").arg(root);
    command
}

/// Run the tool at a root with some arguments.
pub fn run(root: &Path, arguments: &[&str]) -> Output {
    tool(root).args(arguments).output().expect("the tool runs")
}

/// What the tool said on its error stream.
pub fn said(output: &Output) -> String {
    String::from_utf8_lossy(&output.stderr).into_owned()
}

/// A copy, in a folder of its own, of what the tool reads: the fonts'
/// folder, the look's folder and the two licences of the code. The showroom
/// is copied too, which the tool does not read: no release holds it.
pub fn copy_of_repository() -> TempDir {
    let copy = tempfile::tempdir().expect("a temporary folder");
    for folder in ["fonts", "look", "showroom"] {
        let from = repository().join(folder);
        if !from.is_dir() {
            continue;
        }
        let to = copy.path().join(folder);
        fs::create_dir(&to).unwrap();
        for entry in fs::read_dir(from).unwrap() {
            let entry = entry.unwrap();
            if entry.file_type().unwrap().is_file() {
                fs::copy(entry.path(), to.join(entry.file_name())).unwrap();
            }
        }
    }
    for licence in ["LICENSE-MIT", "LICENSE-APACHE"] {
        let source = repository().join(licence);
        if source.is_file() {
            fs::copy(source, copy.path().join(licence)).unwrap();
        }
    }
    copy
}

/// The bytes of a file in the fonts' folder of a root.
pub fn font_file(root: &Path, name: &str) -> Vec<u8> {
    fs::read(root.join("fonts").join(name)).unwrap()
}

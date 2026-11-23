//! The manifest of the fonts, `fonts/manifest.toml`: which build of Cruor
//! the fonts are, and each file's size and SHA-256.
//!
//! A font is a file no one can read by eye, so nothing else would show that
//! one had changed. `manifest --check` does.

use std::fs;
use std::path::{Path, PathBuf};

use serde::Deserialize;
use sha2::{Digest, Sha256};

use crate::families::{self, Family};

/// The manifest, in the fonts' folder.
pub const MANIFEST: &str = "manifest.toml";

/// The manifest as it is read back.
#[derive(Debug, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct Manifest {
    pub source: Source,
    pub font: Vec<Entry>,
}

/// Where the fonts were built.
#[derive(Debug, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct Source {
    /// The commit of the Cruor project the fonts were built at.
    pub commit: String,
}

/// What the manifest records of one font file.
#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct Entry {
    pub file: String,
    pub size: u64,
    pub sha256: String,
}

/// The manifest's path beneath a root.
pub fn path(root: &Path) -> PathBuf {
    families::fonts_dir(root).join(MANIFEST)
}

/// The SHA-256 of some bytes, as sixty-four hexadecimal characters.
pub fn sha256_hex(bytes: &[u8]) -> String {
    Sha256::digest(bytes)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect()
}

/// The size and SHA-256 of a file, under the name it is to be recorded by.
pub fn measure(path: &Path, name: &str) -> Result<Entry, String> {
    let bytes =
        fs::read(path).map_err(|error| format!("cannot read {}: {error}", path.display()))?;
    Ok(Entry {
        file: name.to_string(),
        size: bytes.len() as u64,
        sha256: sha256_hex(&bytes),
    })
}

/// Whether a text is a full commit id: forty hexadecimal characters.
fn is_commit_id(text: &str) -> bool {
    text.len() == 40
        && text
            .chars()
            .all(|c| c.is_ascii_digit() || ('a'..='f').contains(&c))
}

/// The `.woff2` files in the fonts' folder that the list does not call for.
fn unlisted_fonts(root: &Path, families: &[Family]) -> Result<Vec<String>, String> {
    let folder = families::fonts_dir(root);
    let listed = families::font_files(families);
    let entries = fs::read_dir(&folder)
        .map_err(|error| format!("cannot read {}: {error}", folder.display()))?;
    let mut unlisted = Vec::new();
    for entry in entries {
        let entry = entry.map_err(|error| format!("cannot read {}: {error}", folder.display()))?;
        let name = entry.file_name().to_string_lossy().into_owned();
        if name.to_ascii_lowercase().ends_with(".woff2") && !listed.contains(&name) {
            unlisted.push(name);
        }
    }
    unlisted.sort();
    Ok(unlisted)
}

/// Fail, naming them, if the fonts' folder and the list disagree about
/// which fonts there are.
fn require_the_listed_fonts_alone(root: &Path, families: &[Family]) -> Result<(), String> {
    families::require_fonts(root, families)?;
    let unlisted = unlisted_fonts(root, families)?;
    if unlisted.is_empty() {
        return Ok(());
    }
    Err(format!(
        "{} holds what {} does not call for: {}",
        families::fonts_dir(root).display(),
        families::LIST,
        unlisted.join(", ")
    ))
}

/// The entry of every font the list calls for, as the files now are.
fn measure_fonts(root: &Path, families: &[Family]) -> Result<Vec<Entry>, String> {
    let folder = families::fonts_dir(root);
    families::font_files(families)
        .iter()
        .map(|name| measure(&folder.join(name), name))
        .collect()
}

/// The whole text of a manifest.
fn render(commit: &str, entries: &[Entry]) -> String {
    let mut text = format!(
        "# The fonts as they were taken in: which build of Cruor they are, and each\n\
         # file's size and SHA-256.\n\
         #\n\
         # It is made by the framework's tool (`manifest`), and `manifest --check`\n\
         # fails if a font and this record disagree. Do not change it by hand.\n\
         \n\
         [source]\n\
         # The commit of the Cruor project the fonts were built at.\n\
         commit = \"{commit}\"\n"
    );
    for entry in entries {
        text.push_str(&format!(
            "\n[[font]]\nfile = \"{}\"\nsize = {}\nsha256 = \"{}\"\n",
            entry.file, entry.size, entry.sha256
        ));
    }
    text
}

/// Read the manifest beneath a root.
pub fn read(root: &Path) -> Result<Manifest, String> {
    let path = path(root);
    let text = fs::read_to_string(&path)
        .map_err(|error| format!("cannot read {}: {error}", path.display()))?;
    toml::from_str(&text).map_err(|error| format!("{}: {error}", path.display()))
}

/// Write the manifest beneath a root. The commit is the one given or, with
/// none given, the one already recorded; with neither, nothing is written.
pub fn write(root: &Path, source_commit: Option<&str>) -> Result<(), String> {
    let commit = match source_commit {
        Some(given) if is_commit_id(given) => given.to_string(),
        Some(given) => {
            return Err(format!(
                "--source-commit takes a full commit id, forty hexadecimal characters; {given:?} is not one"
            ));
        }
        None if path(root).is_file() => read(root)?.source.commit,
        None => {
            return Err(format!(
                "no commit is known: {} does not exist yet, so give --source-commit",
                path(root).display()
            ));
        }
    };
    let families = families::read(root)?;
    require_the_listed_fonts_alone(root, &families)?;
    let text = render(&commit, &measure_fonts(root, &families)?);
    let path = path(root);
    fs::write(&path, text).map_err(|error| format!("cannot write {}: {error}", path.display()))
}

/// Fail, naming each file at fault, if the fonts and the manifest disagree.
pub fn check(root: &Path) -> Result<(), String> {
    let families = families::read(root)?;
    require_the_listed_fonts_alone(root, &families)?;
    let manifest = read(root)?;
    if !is_commit_id(&manifest.source.commit) {
        return Err(format!(
            "{} records {:?}, which is not a full commit id",
            path(root).display(),
            manifest.source.commit
        ));
    }
    let now = measure_fonts(root, &families)?;

    let mut faults = Vec::new();
    for entry in &now {
        match manifest.font.iter().find(|recorded| recorded.file == entry.file) {
            None => faults.push(format!("{} is not in the manifest", entry.file)),
            Some(recorded) if recorded != entry => faults.push(format!(
                "{} is not the file the manifest records ({} bytes, {}; the manifest has {} bytes, {})",
                entry.file, entry.size, entry.sha256, recorded.size, recorded.sha256
            )),
            Some(_) => {}
        }
    }
    for recorded in &manifest.font {
        if !now.iter().any(|entry| entry.file == recorded.file) {
            faults.push(format!(
                "{} is in the manifest but not in the list",
                recorded.file
            ));
        }
    }
    if faults.is_empty() && manifest.font != now {
        faults.push("the manifest's entries are not in the list's order".to_string());
    }
    if faults.is_empty() {
        return Ok(());
    }
    Err(format!(
        "{} and the fonts disagree: {}",
        path(root).display(),
        faults.join("; ")
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn a_commit_id_is_forty_hexadecimal_characters() {
        assert!(is_commit_id("777120960fd302eb565806badf18a87b49beeffb"));
        assert!(!is_commit_id("7771209"));
        assert!(!is_commit_id("777120960FD302EB565806BADF18A87B49BEEFFB"));
        assert!(!is_commit_id("g77120960fd302eb565806badf18a87b49beeffb"));
        assert!(!is_commit_id(""));
    }

    #[test]
    fn a_checksum_is_the_known_one() {
        assert_eq!(
            sha256_hex(b"abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        );
    }
}

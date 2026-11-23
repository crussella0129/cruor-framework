//! A release, put together in a folder: the fonts, their stylesheet and
//! licence, the licences of the code, a manifest of them all, one archive
//! holding every one of those, and the archive's checksum.
//!
//! A release on GitHub is one flat set of names, so the folder has no
//! folders in it. Everything is worked out before anything is written: a
//! bundle is whole or it is not there.

use std::fs;
use std::io::{Cursor, Write};
use std::path::Path;

use serde::Serialize;
use zip::write::SimpleFileOptions;
use zip::{CompressionMethod, DateTime, System, ZipWriter};

use crate::manifest::{self, sha256_hex};
use crate::{css, families};

/// The framework's version: the crate's.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// The manifest of a release.
pub const RELEASE_MANIFEST: &str = "manifest.json";

/// The licences of the code, at the repository's root.
const CODE_LICENCES: [&str; 2] = ["LICENSE-MIT", "LICENSE-APACHE"];

/// The licence of the fonts, in the fonts' folder.
const FONT_LICENCE: &str = "OFL.txt";

/// The name of a release's archive.
pub fn archive_name() -> String {
    format!("cruor-framework-v{VERSION}.zip")
}

/// The manifest of a release, as it is written.
#[derive(Serialize)]
struct ReleaseManifest<'a> {
    /// The form of this manifest. It goes up if the form ever changes.
    schema: u32,
    framework: &'a str,
    /// The framework's version.
    version: &'a str,
    /// The commit of the Cruor project the fonts were built at.
    cruor_commit: &'a str,
    /// Every file of the release but this manifest and the archive, by name.
    files: Vec<ReleaseFile<'a>>,
}

#[derive(Serialize)]
struct ReleaseFile<'a> {
    name: &'a str,
    size: u64,
    sha256: String,
}

/// Put a release together in `out`.
///
/// Fails, writing nothing, if `tag` is given and is not `v` followed by the
/// framework's version, if `out` holds anything, or if the stylesheet or
/// the manifest of the fonts is not current.
pub fn bundle(root: &Path, out: &Path, tag: Option<&str>) -> Result<(), String> {
    if let Some(tag) = tag {
        let expected = format!("v{VERSION}");
        if tag != expected {
            return Err(format!(
                "the tag {tag:?} is not this version's: the framework is at {VERSION}, whose tag is {expected:?}"
            ));
        }
    }
    require_empty(out)?;

    let faults: Vec<String> = [css::check(root), manifest::check(root)]
        .into_iter()
        .filter_map(Result::err)
        .collect();
    if !faults.is_empty() {
        return Err(format!(
            "no release is put together while a check fails: {}",
            faults.join("; ")
        ));
    }

    // The files of the release, each under its bare name, in name order.
    let families = families::read(root)?;
    let fonts = families::fonts_dir(root);
    let mut files: Vec<(String, Vec<u8>)> = Vec::new();
    let mut take = |folder: &Path, name: &str| -> Result<(), String> {
        let path = folder.join(name);
        let bytes =
            fs::read(&path).map_err(|error| format!("cannot read {}: {error}", path.display()))?;
        files.push((name.to_string(), bytes));
        Ok(())
    };
    for name in families::font_files(&families) {
        take(&fonts, &name)?;
    }
    take(&fonts, css::STYLESHEET)?;
    take(&fonts, FONT_LICENCE)?;
    for name in CODE_LICENCES {
        take(root, name)?;
    }
    files.sort();

    let cruor_commit = manifest::read(root)?.source.commit;
    let release_manifest = ReleaseManifest {
        schema: 1,
        framework: "cruor-framework",
        version: VERSION,
        cruor_commit: &cruor_commit,
        files: files
            .iter()
            .map(|(name, bytes)| ReleaseFile {
                name,
                size: bytes.len() as u64,
                sha256: sha256_hex(bytes),
            })
            .collect(),
    };
    let mut manifest_json = serde_json::to_string_pretty(&release_manifest)
        .map_err(|error| format!("cannot write {RELEASE_MANIFEST}: {error}"))?;
    manifest_json.push('\n');
    files.push((RELEASE_MANIFEST.to_string(), manifest_json.into_bytes()));
    files.sort();

    let archive = archive(&files)?;
    let archive_name = archive_name();
    let checksum = format!("{}  {}\n", sha256_hex(&archive), archive_name);
    files.push((archive_name.clone(), archive));
    files.push((format!("{archive_name}.sha256"), checksum.into_bytes()));

    fs::create_dir_all(out).map_err(|error| format!("cannot make {}: {error}", out.display()))?;
    for (name, bytes) in &files {
        let path = out.join(name);
        fs::write(&path, bytes)
            .map_err(|error| format!("cannot write {}: {error}", path.display()))?;
    }
    Ok(())
}

/// Fail unless a folder is absent or empty.
fn require_empty(out: &Path) -> Result<(), String> {
    if !out.exists() {
        return Ok(());
    }
    let mut entries =
        fs::read_dir(out).map_err(|error| format!("cannot read {}: {error}", out.display()))?;
    if entries.next().is_some() {
        return Err(format!(
            "{} is not empty; a release is put together in a folder of its own",
            out.display()
        ));
    }
    Ok(())
}

/// One archive of some files, the same bytes every time and on every
/// system: the entries in the order given, stored as they are, each with
/// the same time and the same permissions, and marked as one system's.
fn archive(files: &[(String, Vec<u8>)]) -> Result<Vec<u8>, String> {
    let options = SimpleFileOptions::default()
        .compression_method(CompressionMethod::Stored)
        .last_modified_time(DateTime::DEFAULT)
        .system(System::Unix)
        .unix_permissions(0o644);
    let failed = |error: &dyn std::fmt::Display| format!("cannot make the archive: {error}");
    let mut writer = ZipWriter::new(Cursor::new(Vec::new()));
    for (name, bytes) in files {
        writer
            .start_file(name.as_str(), options)
            .map_err(|error| failed(&error))?;
        writer.write_all(bytes).map_err(|error| failed(&error))?;
    }
    let cursor = writer.finish().map_err(|error| failed(&error))?;
    Ok(cursor.into_inner())
}

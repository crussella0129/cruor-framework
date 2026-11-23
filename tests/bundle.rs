//! The `bundle` command, run for real on a copy of the repository's files.

mod common;

use std::collections::BTreeMap;
use std::fs;
use std::io::Read;
use std::path::Path;

use common::{copy_of_repository, repository, run, said};
use sha2::{Digest, Sha256};
use tempfile::TempDir;

const VERSION: &str = env!("CARGO_PKG_VERSION");

fn archive_name() -> String {
    format!("cruor-framework-v{VERSION}.zip")
}

fn sha256_hex(bytes: &[u8]) -> String {
    Sha256::digest(bytes)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect()
}

/// Every file in a folder, by name; fails if the folder holds a folder.
fn files_in(folder: &Path) -> BTreeMap<String, Vec<u8>> {
    fs::read_dir(folder)
        .unwrap()
        .map(|entry| {
            let entry = entry.unwrap();
            assert!(
                entry.file_type().unwrap().is_file(),
                "{:?} is not a file: a release has no folders",
                entry.file_name()
            );
            (
                entry.file_name().into_string().unwrap(),
                fs::read(entry.path()).unwrap(),
            )
        })
        .collect()
}

/// The names the fonts' folder gives the thirty-two fonts.
fn font_names() -> Vec<String> {
    let mut names: Vec<String> = fs::read_dir(repository().join("fonts"))
        .unwrap()
        .map(|entry| entry.unwrap().file_name().into_string().unwrap())
        .filter(|name| name.ends_with(".woff2"))
        .collect();
    names.sort();
    assert_eq!(names.len(), 32);
    names
}

/// What a release holds beside its manifest, its archive and the archive's
/// checksum: the fonts, their stylesheet and licence, the code's licences.
fn carried_names() -> Vec<String> {
    let mut names = font_names();
    for name in ["fonts.css", "OFL.txt", "LICENSE-MIT", "LICENSE-APACHE"] {
        names.push(name.to_string());
    }
    names.sort();
    names
}

/// A bundle of a fresh copy of the repository: the copy, and the folder.
fn a_bundle() -> (TempDir, TempDir) {
    let copy = copy_of_repository();
    let out = tempfile::tempdir().unwrap();
    let output = run(
        copy.path(),
        &["bundle", "--out", out.path().to_str().unwrap()],
    );
    assert!(output.status.success(), "{}", said(&output));
    (copy, out)
}

#[test]
fn bundle_holds_expected_files() {
    let (_copy, out) = a_bundle();
    let mut expected = carried_names();
    expected.push("manifest.json".to_string());
    expected.push(archive_name());
    expected.push(format!("{}.sha256", archive_name()));
    expected.sort();
    let found: Vec<String> = files_in(out.path()).into_keys().collect();
    assert_eq!(found, expected);
    assert_eq!(found.len(), 39);
}

#[test]
fn bundle_archive_holds_same_files() {
    let (_copy, out) = a_bundle();
    let beside = files_in(out.path());
    let reader = fs::File::open(out.path().join(archive_name())).unwrap();
    let mut archive = zip::ZipArchive::new(reader).unwrap();

    let mut inside = BTreeMap::new();
    for index in 0..archive.len() {
        let mut entry = archive.by_index(index).unwrap();
        let mut bytes = Vec::new();
        entry.read_to_end(&mut bytes).unwrap();
        inside.insert(entry.name().unwrap().into_owned(), bytes);
    }

    let mut expected = carried_names();
    expected.push("manifest.json".to_string());
    expected.sort();
    assert_eq!(inside.keys().cloned().collect::<Vec<_>>(), expected);
    for (name, bytes) in &inside {
        assert_eq!(bytes, &beside[name], "{name} is the same in the archive");
    }
}

#[test]
fn bundle_archive_checksum_is_right() {
    let (_copy, out) = a_bundle();
    let files = files_in(out.path());
    let checksum = String::from_utf8(files[&format!("{}.sha256", archive_name())].clone()).unwrap();
    assert_eq!(
        checksum,
        format!(
            "{}  {}\n",
            sha256_hex(&files[&archive_name()]),
            archive_name()
        )
    );
}

#[test]
fn bundle_manifest_matches_files() {
    let (copy, out) = a_bundle();
    let files = files_in(out.path());
    let manifest: serde_json::Value = serde_json::from_slice(&files["manifest.json"]).unwrap();

    assert_eq!(manifest["version"], VERSION);
    assert_eq!(manifest["framework"], "cruor-framework");
    let fonts_manifest: toml::Table = fs::read_to_string(copy.path().join("fonts/manifest.toml"))
        .unwrap()
        .parse()
        .unwrap();
    assert_eq!(
        manifest["cruor_commit"].as_str().unwrap(),
        fonts_manifest["source"]["commit"].as_str().unwrap()
    );

    let listed = manifest["files"].as_array().unwrap();
    let names: Vec<&str> = listed
        .iter()
        .map(|file| file["name"].as_str().unwrap())
        .collect();
    assert_eq!(
        names,
        carried_names(),
        "the files carried, and nothing else"
    );
    for file in listed {
        let bytes = &files[file["name"].as_str().unwrap()];
        assert_eq!(file["size"].as_u64().unwrap(), bytes.len() as u64);
        assert_eq!(file["sha256"].as_str().unwrap(), sha256_hex(bytes));
    }
}

#[test]
fn bundle_carries_the_repository_files_unchanged() {
    let (_copy, out) = a_bundle();
    let files = files_in(out.path());
    for name in font_names()
        .iter()
        .map(String::as_str)
        .chain(["fonts.css", "OFL.txt"])
    {
        assert_eq!(
            files[name],
            fs::read(repository().join("fonts").join(name)).unwrap()
        );
    }
    for name in ["LICENSE-MIT", "LICENSE-APACHE"] {
        assert_eq!(files[name], fs::read(repository().join(name)).unwrap());
    }
}

#[test]
fn bundle_is_reproducible() {
    let (_first_copy, first) = a_bundle();
    let (_second_copy, second) = a_bundle();
    let (first, second) = (files_in(first.path()), files_in(second.path()));
    for name in [
        "manifest.json".to_string(),
        archive_name(),
        format!("{}.sha256", archive_name()),
    ] {
        assert_eq!(first[&name], second[&name], "{name} is the same both times");
    }
    assert_eq!(first, second);
}

#[test]
fn bundle_refuses_when_a_check_fails() {
    // A stale stylesheet.
    let copy = copy_of_repository();
    let css = copy.path().join("fonts/fonts.css");
    let stale = fs::read_to_string(&css)
        .unwrap()
        .replacen("swap", "block", 1);
    fs::write(&css, stale).unwrap();
    let out = tempfile::tempdir().unwrap();
    let output = run(
        copy.path(),
        &["bundle", "--out", out.path().to_str().unwrap()],
    );
    assert!(!output.status.success());
    assert!(said(&output).contains("fonts.css"), "{}", said(&output));
    assert!(files_in(out.path()).is_empty(), "nothing is written");

    // A changed font, into a folder that does not exist yet.
    let copy = copy_of_repository();
    let font = copy.path().join("fonts/CruorSansPixelated-Italic.woff2");
    let mut bytes = fs::read(&font).unwrap();
    bytes[10] ^= 1;
    fs::write(&font, bytes).unwrap();
    let parent = tempfile::tempdir().unwrap();
    let out = parent.path().join("release");
    let output = run(copy.path(), &["bundle", "--out", out.to_str().unwrap()]);
    assert!(!output.status.success());
    assert!(
        said(&output).contains("CruorSansPixelated-Italic.woff2"),
        "{}",
        said(&output)
    );
    assert!(!out.exists(), "nothing is written");
}

#[test]
fn bundle_refuses_nonempty_folder() {
    let copy = copy_of_repository();
    let out = tempfile::tempdir().unwrap();
    fs::write(out.path().join("something.txt"), b"already here\n").unwrap();
    let output = run(
        copy.path(),
        &["bundle", "--out", out.path().to_str().unwrap()],
    );
    assert!(!output.status.success());
    assert!(said(&output).contains("not empty"), "{}", said(&output));
    let files = files_in(out.path());
    assert_eq!(files.len(), 1);
    assert_eq!(files["something.txt"], b"already here\n");
}

#[test]
fn bundle_css_addresses_are_bare_and_present() {
    let (_copy, out) = a_bundle();
    let files = files_in(out.path());
    let css = String::from_utf8(files["fonts.css"].clone()).unwrap();
    let addresses: Vec<&str> = css
        .split("url(\"")
        .skip(1)
        .map(|rest| rest.split('"').next().unwrap())
        .collect();
    assert_eq!(addresses.len(), 32);
    assert_eq!(css.matches("url(").count(), 32, "every address is quoted");
    for address in addresses {
        assert!(
            !address.contains(['/', '\\', ':']),
            "{address} is a bare file name"
        );
        assert!(files.contains_key(address), "{address} is in the release");
    }
}

#[test]
fn bundle_refuses_mismatched_tag() {
    let copy = copy_of_repository();
    for tag in ["v9.9.9", VERSION, "v", &format!("v{VERSION}-rc.1")] {
        let parent = tempfile::tempdir().unwrap();
        let out = parent.path().join("release");
        let output = run(
            copy.path(),
            &["bundle", "--out", out.to_str().unwrap(), "--tag", tag],
        );
        assert!(!output.status.success(), "refuses the tag {tag:?}");
        assert!(said(&output).contains("tag"), "{}", said(&output));
        assert!(!out.exists(), "nothing is written");
    }
}

#[test]
fn bundle_accepts_matching_tag() {
    let copy = copy_of_repository();
    let out = tempfile::tempdir().unwrap();
    let tag = format!("v{VERSION}");
    let output = run(
        copy.path(),
        &[
            "bundle",
            "--out",
            out.path().to_str().unwrap(),
            "--tag",
            &tag,
        ],
    );
    assert!(output.status.success(), "{}", said(&output));
    assert_eq!(files_in(out.path()).len(), 39);
}

//! The `manifest` and `check` commands, run for real on a copy of the fonts'
//! folder.

mod common;

use std::fs;
use std::path::Path;

use common::{copy_of_repository, font_file, repository, run, said};
use sha2::{Digest, Sha256};

/// A full commit id that is not the one the repository records.
const A_COMMIT: &str = "0123456789abcdef0123456789abcdef01234567";

fn sha256_hex(bytes: &[u8]) -> String {
    Sha256::digest(bytes)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect()
}

fn manifest(root: &Path) -> toml::Table {
    fs::read_to_string(root.join("fonts/manifest.toml"))
        .unwrap()
        .parse()
        .unwrap()
}

fn commit_of(root: &Path) -> String {
    manifest(root)["source"]["commit"]
        .as_str()
        .unwrap()
        .to_string()
}

#[test]
fn manifest_records_every_font() {
    let copy = copy_of_repository();
    fs::remove_file(copy.path().join("fonts/manifest.toml")).unwrap();
    let output = run(copy.path(), &["manifest", "--source-commit", A_COMMIT]);
    assert!(output.status.success(), "{}", said(&output));

    assert_eq!(commit_of(copy.path()), A_COMMIT);
    let manifest = manifest(copy.path());
    let fonts = manifest["font"].as_array().unwrap();
    assert_eq!(fonts.len(), 32);
    for font in fonts {
        let name = font["file"].as_str().unwrap();
        let bytes = font_file(copy.path(), name);
        assert_eq!(font["size"].as_integer().unwrap(), bytes.len() as i64);
        assert_eq!(font["sha256"].as_str().unwrap(), sha256_hex(&bytes));
    }
    let mut names: Vec<_> = fonts
        .iter()
        .map(|font| font["file"].as_str().unwrap())
        .collect();
    names.sort();
    names.dedup();
    assert_eq!(names.len(), 32, "each font once");
}

#[test]
fn manifest_refuses_short_commit() {
    let copy = copy_of_repository();
    let before = font_file(copy.path(), "manifest.toml");
    for not_an_id in ["abc1234", "", "the head of the working branch"] {
        let output = run(copy.path(), &["manifest", "--source-commit", not_an_id]);
        assert!(!output.status.success(), "refuses {not_an_id:?}");
        assert!(said(&output).contains("forty"), "{}", said(&output));
    }
    assert_eq!(font_file(copy.path(), "manifest.toml"), before);
}

#[test]
fn manifest_refuses_when_no_commit_known() {
    let copy = copy_of_repository();
    let path = copy.path().join("fonts/manifest.toml");
    fs::remove_file(&path).unwrap();
    let output = run(copy.path(), &["manifest"]);
    assert!(!output.status.success());
    assert!(
        said(&output).contains("--source-commit"),
        "{}",
        said(&output)
    );
    assert!(!path.exists(), "nothing is written");
}

#[test]
fn manifest_check_fails_on_changed_byte() {
    let copy = copy_of_repository();
    assert!(run(copy.path(), &["manifest", "--check"]).status.success());

    let path = copy.path().join("fonts/CruorPixelated-Bold.woff2");
    let mut bytes = fs::read(&path).unwrap();
    let last = bytes.len() - 1;
    bytes[last] ^= 1;
    fs::write(&path, bytes).unwrap();

    let output = run(copy.path(), &["manifest", "--check"]);
    assert!(!output.status.success());
    assert!(
        said(&output).contains("CruorPixelated-Bold.woff2"),
        "{}",
        said(&output)
    );
}

#[test]
fn manifest_check_fails_on_missing_font() {
    let copy = copy_of_repository();
    fs::remove_file(copy.path().join("fonts/CruorSansRegular-Regular.woff2")).unwrap();
    let output = run(copy.path(), &["manifest", "--check"]);
    assert!(!output.status.success());
    assert!(
        said(&output).contains("CruorSansRegular-Regular.woff2"),
        "{}",
        said(&output)
    );
}

#[test]
fn manifest_check_fails_on_unlisted_font() {
    let copy = copy_of_repository();
    fs::copy(
        copy.path().join("fonts/CruorSansMono-Regular.woff2"),
        copy.path().join("fonts/CruorSansMono-Light.woff2"),
    )
    .unwrap();
    let output = run(copy.path(), &["manifest", "--check"]);
    assert!(!output.status.success());
    assert!(
        said(&output).contains("CruorSansMono-Light.woff2"),
        "{}",
        said(&output)
    );
}

#[test]
fn manifest_keeps_source_commit() {
    let copy = copy_of_repository();
    assert!(
        run(copy.path(), &["manifest", "--source-commit", A_COMMIT])
            .status
            .success()
    );
    assert!(run(copy.path(), &["manifest"]).status.success());
    assert_eq!(commit_of(copy.path()), A_COMMIT);
}

#[test]
fn check_runs_both() {
    let copy = copy_of_repository();
    assert!(run(copy.path(), &["check"]).status.success());

    // Only the stylesheet is stale.
    let css = copy.path().join("fonts/fonts.css");
    let good = fs::read(&css).unwrap();
    fs::write(&css, b"/* nothing */\n").unwrap();
    let output = run(copy.path(), &["check"]);
    assert!(!output.status.success());
    assert!(said(&output).contains("fonts.css"), "{}", said(&output));
    assert!(
        !said(&output).contains("manifest.toml"),
        "{}",
        said(&output)
    );
    fs::write(&css, good).unwrap();

    // Only the manifest is stale.
    let font = copy.path().join("fonts/CruorLiteRegular-Italic.woff2");
    let mut bytes = fs::read(&font).unwrap();
    bytes[0] ^= 1;
    fs::write(&font, bytes).unwrap();
    let output = run(copy.path(), &["check"]);
    assert!(!output.status.success());
    assert!(said(&output).contains("manifest.toml"), "{}", said(&output));
    assert!(!said(&output).contains("fonts.css"), "{}", said(&output));
}

#[test]
fn repository_passes_check() {
    let output = run(&repository(), &["check"]);
    assert!(output.status.success(), "{}", said(&output));
}

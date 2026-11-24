//! The theme file and its form: `look --check`, run for real on the
//! repository's theme and on copies spoiled one way at a time.

mod common;

use std::fs;
use std::path::Path;

use common::{copy_of_repository, repository, run, said};

/// What the form requires, as the sprint's plan names it. The list is the
/// plan's and not the tool's, so the tool cannot pass by forgetting a key.
const FONT_ROLES: [&str; 4] = ["title", "heading", "text", "code"];
const COLOUR_ROLES: [&str; 22] = [
    "page",
    "panel",
    "sunken",
    "text",
    "text-subdued",
    "text-bright",
    "border",
    "border-subdued",
    "accent",
    "accent-subdued",
    "link",
    "inscription",
    "inscription-link",
    "heading-top",
    "heading-foot",
    "selection",
    "chip-top",
    "chip-foot",
    "blood",
    "blood-edge",
    "shadow",
    "vignette",
];
const VOID_ROLES: [&str; 8] = [
    "ground",
    "sunken",
    "row",
    "text",
    "text-subdued",
    "accent",
    "channel",
    "border",
];
const STONE_KEYS: [&str; 4] = ["sheen", "sheen-opacity", "candle", "candle-opacity"];
const MEASURES: [&str; 6] = [
    "inscription-size",
    "interface-size",
    "line",
    "column",
    "seal-size",
    "seal-font",
];
const LEVELS: [&str; 6] = ["h1", "h2", "h3", "h4", "h5", "h6"];
const HEADING_KEYS: [&str; 5] = ["font", "bold", "italic", "underline", "size"];

fn theme_path(root: &Path) -> std::path::PathBuf {
    root.join("look/theme.toml")
}

/// Change the theme file of a copy: one piece of its text for another.
fn change(root: &Path, old: &str, new: &str) {
    let path = theme_path(root);
    let text = fs::read_to_string(&path).unwrap();
    assert_eq!(text.matches(old).count(), 1, "{old:?} is in the theme once");
    fs::write(&path, text.replace(old, new)).unwrap();
}

/// Run `look --check` on a copy and expect a refusal that names a key.
fn refused(root: &Path, key: &str) {
    let output = run(root, &["look", "--check"]);
    assert!(!output.status.success(), "the theme is refused");
    let message = said(&output);
    assert!(
        message.contains(&format!("look/theme.toml: {key}: ")),
        "{key} is named in: {message}"
    );
}

#[test]
fn theme_as_written_is_complete() {
    let output = run(&repository(), &["look", "--check"]);
    assert!(output.status.success(), "{}", said(&output));

    let table: toml::Table = fs::read_to_string(theme_path(&repository()))
        .unwrap()
        .parse()
        .unwrap();
    for key in ["name", "class"] {
        assert!(table[key].is_str(), "{key}");
    }
    for role in FONT_ROLES {
        assert!(table["font"][role].is_str(), "font.{role}");
    }
    for role in COLOUR_ROLES {
        assert!(table["colour"][role].is_str(), "colour.{role}");
    }
    for role in VOID_ROLES {
        assert!(table["void"][role].is_str(), "void.{role}");
    }
    for key in STONE_KEYS {
        assert!(table["stone"].get(key).is_some(), "stone.{key}");
    }
    for key in MEASURES {
        assert!(table["measure"].get(key).is_some(), "measure.{key}");
    }
    for level in LEVELS {
        for key in HEADING_KEYS {
            assert!(
                table["heading"][level].get(key).is_some(),
                "heading.{level}.{key}"
            );
        }
    }
}

#[test]
fn theme_refuses_a_missing_key() {
    let copy = copy_of_repository();
    change(
        copy.path(),
        "inscription = \"#d50210\"        # running text, at 24 pixels or more\n",
        "",
    );
    refused(copy.path(), "colour.inscription");

    let copy = copy_of_repository();
    change(copy.path(), "seal-size = 3.4", "# seal-size = 3.4");
    refused(copy.path(), "measure.seal-size");

    let copy = copy_of_repository();
    change(
        copy.path(),
        "[heading.h4]\nfont = \"heading\"\nbold = true\n",
        "[heading.h4]\nfont = \"heading\"\n",
    );
    refused(copy.path(), "heading.h4.bold");
}

#[test]
fn theme_refuses_an_unknown_key() {
    let copy = copy_of_repository();
    change(copy.path(), "[colour]\n", "[colour]\nink = \"#d50210\"\n");
    refused(copy.path(), "colour.ink");

    let copy = copy_of_repository();
    change(copy.path(), "[font]\n", "motto = \"sanguis\"\n\n[font]\n");
    refused(copy.path(), "motto");
}

#[test]
fn theme_refuses_a_bad_colour() {
    let copy = copy_of_repository();
    change(copy.path(), "page = \"#0a0708\"", "page = \"#12\"");
    refused(copy.path(), "colour.page");

    let copy = copy_of_repository();
    change(
        copy.path(),
        "row = \"rgba(213, 2, 16, 0.22)\"",
        "row = \"rgba(213, 2, 16)\"",
    );
    refused(copy.path(), "void.row");
}

#[test]
fn theme_refuses_a_family_the_kit_does_not_hold() {
    let copy = copy_of_repository();
    change(
        copy.path(),
        "text = \"Cruor Sans Regular\"",
        "text = \"Cruor Sans Narrow\"",
    );
    refused(copy.path(), "font.text");
}

#[test]
fn theme_refuses_a_heading_font_that_is_neither() {
    let copy = copy_of_repository();
    change(
        copy.path(),
        "[heading.h2]\nfont = \"heading\"",
        "[heading.h2]\nfont = \"captions\"",
    );
    refused(copy.path(), "heading.h2.font");
}

#[test]
fn theme_refuses_a_seal_font_that_is_neither() {
    let copy = copy_of_repository();
    change(
        copy.path(),
        "seal-font = \"title\"",
        "seal-font = \"captions\"",
    );
    refused(copy.path(), "measure.seal-font");
}

#[test]
fn theme_accepts_a_heading_font_by_family() {
    let copy = copy_of_repository();
    change(
        copy.path(),
        "[heading.h2]\nfont = \"heading\"",
        "[heading.h2]\nfont = \"Cruor Pixelated\"",
    );
    // The theme is taken, and the tokens made from it set that level in
    // the family named.
    let output = run(copy.path(), &["look"]);
    assert!(output.status.success(), "{}", said(&output));
    let tokens = fs::read_to_string(copy.path().join("look/tokens.css")).unwrap();
    assert!(
        tokens.contains("--cruor-h2-font: \"Cruor Pixelated\";"),
        "{tokens}"
    );
    assert!(run(copy.path(), &["look", "--check"]).status.success());
}

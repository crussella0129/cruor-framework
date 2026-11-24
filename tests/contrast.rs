//! The contrast the theme file promises: that the promises are all there,
//! that the look as written keeps them, and that a look which does not is
//! refused by name. Run for real on copies of the repository.

mod common;

use std::fs;
use std::path::Path;

use common::{copy_of_repository, repository, run, said};

/// Every pair the sprint's plan says the theme must promise, with its
/// ratio. The list is the plan's and not the theme's.
const BOUNDS: [(&[&str], &[&str], f64); 10] = [
    (
        &["inscription", "inscription-link"],
        &["page", "stone", "panel"],
        3.3,
    ),
    (
        &["text", "text-subdued", "link", "accent"],
        &["page", "stone", "panel", "sunken"],
        4.5,
    ),
    (&["heading-top", "heading-foot"], &["page"], 3.0),
    (&["heading-top"], &["stone"], 3.0),
    (&["chip-top", "chip-foot"], &["sunken"], 4.5),
    (&["text-bright"], &["selection"], 4.5),
    (
        &["void.text", "void.text-subdued", "void.accent"],
        &["void.ground", "void.sunken"],
        4.5,
    ),
    (
        &["void.text", "void.accent"],
        &["void.row", "void.sunken-row"],
        4.5,
    ),
    (&["void.channel"], &["void.ground", "void.sunken"], 3.0),
    (&["blood-edge"], &["page", "stone", "panel", "sunken"], 3.0),
];

fn theme_path(root: &Path) -> std::path::PathBuf {
    root.join("look/theme.toml")
}

fn change(root: &Path, old: &str, new: &str) {
    let path = theme_path(root);
    let text = fs::read_to_string(&path).unwrap();
    assert_eq!(text.matches(old).count(), 1, "{old:?} is in the theme once");
    fs::write(&path, text.replace(old, new)).unwrap();
}

fn names(value: &toml::Value) -> Vec<String> {
    value
        .as_array()
        .unwrap()
        .iter()
        .map(|name| name.as_str().unwrap().to_string())
        .collect()
}

#[test]
fn contrast_names_every_bound_of_the_look() {
    let theme: toml::Table = fs::read_to_string(theme_path(&repository()))
        .unwrap()
        .parse()
        .unwrap();
    let entries = theme["contrast"].as_array().unwrap();
    for (texts, grounds, bound) in BOUNDS {
        for text in texts {
            for ground in grounds {
                let covered = entries.iter().any(|entry| {
                    names(&entry["text"]).iter().any(|name| name == text)
                        && names(&entry["grounds"]).iter().any(|name| name == ground)
                        && entry["at-least"].as_float().unwrap() >= bound
                });
                assert!(covered, "{text} on {ground} at {bound} is promised");
            }
        }
    }
}

#[test]
fn contrast_holds_for_the_look() {
    let output = run(&repository(), &["look", "--check"]);
    assert!(output.status.success(), "{}", said(&output));
}

#[test]
fn contrast_fails_naming_the_pair() {
    // The inscription dimmed until it cannot be read on the panel.
    let copy = copy_of_repository();
    change(
        copy.path(),
        "inscription = \"#d50210\"",
        "inscription = \"#8a0109\"",
    );
    let output = run(copy.path(), &["look", "--check"]);
    assert!(!output.status.success());
    let message = said(&output);
    assert!(message.contains("look/theme.toml: "), "{message}");
    // The text role, the ground, the ratio to two places and the bound.
    let told = message
        .lines()
        .find(|line| line.contains("inscription on panel stands at "))
        .unwrap_or_else(|| panic!("the pair is named in: {message}"));
    let ratio = told
        .split("stands at ")
        .nth(1)
        .unwrap()
        .split(',')
        .next()
        .unwrap();
    assert_eq!(ratio.split('.').nth(1).map(str::len), Some(2), "{ratio}");
    let ratio: f64 = ratio.parse().unwrap();
    assert!(ratio > 1.0 && ratio < 3.3, "{ratio}");
    assert!(told.ends_with("and 3.3 is promised"), "{told}");
    // Each ground it fails on is told, not the first alone.
    assert!(message.contains("inscription on stone stands at "));
    assert!(message.contains("inscription on page stands at "));
}

#[test]
fn look_refuses_a_theme_that_fails_contrast() {
    let copy = copy_of_repository();
    let tokens = copy.path().join("look/tokens.css");
    let before = fs::read(&tokens).unwrap();
    change(
        copy.path(),
        "inscription = \"#d50210\"",
        "inscription = \"#8a0109\"",
    );
    let output = run(copy.path(), &["look"]);
    assert!(!output.status.success());
    assert_eq!(fs::read(&tokens).unwrap(), before, "nothing is written");

    // Nor is anything written where there was nothing before.
    fs::remove_file(&tokens).unwrap();
    assert!(!run(copy.path(), &["look"]).status.success());
    assert!(!tokens.exists());
}

#[test]
fn contrast_refuses_an_unknown_role() {
    let copy = copy_of_repository();
    change(
        copy.path(),
        "text = [\"inscription\", \"inscription-link\"]",
        "text = [\"inscripton\", \"inscription-link\"]",
    );
    let output = run(copy.path(), &["look", "--check"]);
    assert!(!output.status.success());
    assert!(
        said(&output).contains("\"inscripton\" is no text role of the theme"),
        "{}",
        said(&output)
    );

    let copy = copy_of_repository();
    change(
        copy.path(),
        "grounds = [\"page\", \"stone\", \"panel\"]",
        "grounds = [\"page\", \"stones\", \"panel\"]",
    );
    let output = run(copy.path(), &["look", "--check"]);
    assert!(!output.status.success());
    assert!(
        said(&output).contains("\"stones\" is no ground of the theme"),
        "{}",
        said(&output)
    );
}

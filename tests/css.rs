//! The `css` command, run for real on a copy of the fonts' folder.

mod common;

use std::fs;

use common::{copy_of_repository, font_file, repository, run, said};

#[test]
fn css_writes_what_the_repository_holds() {
    let copy = copy_of_repository();
    fs::remove_file(copy.path().join("fonts/fonts.css")).unwrap();
    assert!(run(copy.path(), &["css"]).status.success());
    assert_eq!(
        font_file(copy.path(), "fonts.css"),
        font_file(&repository(), "fonts.css"),
        "the tracked stylesheet is what `css` writes"
    );
}

#[test]
fn css_check_fails_when_stale() {
    let copy = copy_of_repository();
    assert!(run(copy.path(), &["css", "--check"]).status.success());

    let path = copy.path().join("fonts/fonts.css");
    let stale =
        fs::read_to_string(&path)
            .unwrap()
            .replacen("font-weight: 700", "font-weight: 600", 1);
    fs::write(&path, &stale).unwrap();

    let output = run(copy.path(), &["css", "--check"]);
    assert!(!output.status.success());
    assert!(said(&output).contains("fonts.css"), "{}", said(&output));
    assert_eq!(
        fs::read_to_string(&path).unwrap(),
        stale,
        "a check changes nothing"
    );
}

#[test]
fn css_fails_on_missing_font() {
    for arguments in [&["css"][..], &["css", "--check"][..]] {
        let copy = copy_of_repository();
        fs::remove_file(copy.path().join("fonts/CruorLiteMono-Italic.woff2")).unwrap();
        let before = font_file(copy.path(), "fonts.css");

        let output = run(copy.path(), arguments);
        assert!(!output.status.success());
        assert!(
            said(&output).contains("CruorLiteMono-Italic.woff2"),
            "{}",
            said(&output)
        );
        assert_eq!(font_file(copy.path(), "fonts.css"), before);
    }
}

#[test]
fn css_is_deterministic() {
    let copy = copy_of_repository();
    assert!(run(copy.path(), &["css"]).status.success());
    let first = font_file(copy.path(), "fonts.css");
    assert!(run(copy.path(), &["css"]).status.success());
    let second = font_file(copy.path(), "fonts.css");
    assert_eq!(first, second);
    assert!(!first.contains(&b'\r'), "line feeds alone");
    assert!(first.ends_with(b"}\n"));
}

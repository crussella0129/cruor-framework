//! The `look` command: the tokens made from the theme file, and the check
//! that holds the two together. Run for real on copies of the repository.

mod common;

use std::fs;
use std::path::Path;

use common::{copy_of_repository, repository, run, said};

fn tokens_path(root: &Path) -> std::path::PathBuf {
    root.join("look/tokens.css")
}

fn theme(root: &Path) -> toml::Table {
    fs::read_to_string(root.join("look/theme.toml"))
        .unwrap()
        .parse()
        .unwrap()
}

/// The declarations of the tokens' one rule, as (property, value).
fn declarations(css: &str) -> Vec<(String, String)> {
    let open = css.find('{').expect("the rule opens");
    let close = css.rfind('}').expect("the rule closes");
    css[open + 1..close]
        .lines()
        .map(str::trim)
        .filter(|line| !line.is_empty())
        .map(|line| {
            let (property, value) = line.split_once(": ").expect("a declaration");
            (
                property.to_string(),
                value.strip_suffix(';').expect("it ends").to_string(),
            )
        })
        .collect()
}

/// A value of the theme file as a stylesheet writes it.
fn written(value: &toml::Value) -> String {
    match value {
        toml::Value::String(text) => text.clone(),
        toml::Value::Float(number) => number.to_string(),
        toml::Value::Integer(number) => number.to_string(),
        other => panic!("{other:?} is not written in a token"),
    }
}

/// The family a font reference comes to: a role's family, or the name.
fn family(theme: &toml::Table, named: &str) -> String {
    match theme["font"].get(named) {
        Some(family) => format!("\"{}\"", family.as_str().unwrap()),
        None => format!("\"{named}\""),
    }
}

#[test]
fn tokens_hold_every_role() {
    let copy = copy_of_repository();
    fs::remove_file(tokens_path(copy.path())).unwrap();
    let output = run(copy.path(), &["look"]);
    assert!(output.status.success(), "{}", said(&output));

    let theme = theme(copy.path());
    let mut expected: Vec<(String, String)> = Vec::new();
    for (role, colour) in theme["colour"].as_table().unwrap() {
        expected.push((format!("--cruor-{role}"), written(colour)));
    }
    for (role, colour) in theme["void"].as_table().unwrap() {
        expected.push((format!("--cruor-void-{role}"), written(colour)));
    }
    for (key, value) in theme["stone"].as_table().unwrap() {
        expected.push((format!("--cruor-stone-{key}"), written(value)));
    }
    for (role, name) in theme["font"].as_table().unwrap() {
        expected.push((
            format!("--cruor-font-{role}"),
            format!("\"{}\"", name.as_str().unwrap()),
        ));
    }
    for (key, value) in theme["measure"].as_table().unwrap() {
        let value = if key == "seal-font" {
            family(&theme, value.as_str().unwrap())
        } else {
            written(value)
        };
        expected.push((format!("--cruor-{key}"), value));
    }
    for (level, settings) in theme["heading"].as_table().unwrap() {
        let on = |key: &str, yes: &str, no: &str| {
            if settings[key].as_bool().unwrap() {
                yes.to_string()
            } else {
                no.to_string()
            }
        };
        expected.push((
            format!("--cruor-{level}-font"),
            family(&theme, settings["font"].as_str().unwrap()),
        ));
        expected.push((format!("--cruor-{level}-weight"), on("bold", "700", "400")));
        expected.push((
            format!("--cruor-{level}-style"),
            on("italic", "italic", "normal"),
        ));
        expected.push((
            format!("--cruor-{level}-decoration"),
            on("underline", "underline", "none"),
        ));
        expected.push((format!("--cruor-{level}-size"), written(&settings["size"])));
    }
    // 22 colours, 8 of the void, 4 of the stone, 4 fonts, 6 measures, and
    // five settings for each of six levels.
    assert_eq!(expected.len(), 22 + 8 + 4 + 4 + 6 + 30);

    let mut found = declarations(&fs::read_to_string(tokens_path(copy.path())).unwrap());
    found.sort();
    expected.sort();
    assert_eq!(found, expected);
}

#[test]
fn tokens_are_one_rule_on_the_class() {
    let css = fs::read_to_string(tokens_path(&repository())).unwrap();
    let class = theme(&repository())["class"].as_str().unwrap().to_string();

    // Take the comment at the head away; what is left is the one rule.
    let rule = css[css.find("*/").expect("a comment at the head") + 2..].trim();
    assert!(rule.starts_with(&format!(".{class} {{\n")), "{rule}");
    assert!(rule.ends_with("\n}"));
    assert_eq!(rule.matches('{').count(), 1, "one rule and no more");
    assert_eq!(rule.matches('}').count(), 1);
    for (property, _) in declarations(&css) {
        assert!(property.starts_with("--cruor-"), "{property}");
    }
}

#[test]
fn tokens_are_the_same_twice() {
    let copy = copy_of_repository();
    assert!(run(copy.path(), &["look"]).status.success());
    let first = fs::read(tokens_path(copy.path())).unwrap();
    fs::remove_file(tokens_path(copy.path())).unwrap();
    assert!(run(copy.path(), &["look"]).status.success());
    let second = fs::read(tokens_path(copy.path())).unwrap();
    assert_eq!(first, second);
    assert!(!first.contains(&b'\r'), "line feeds alone");
}

#[test]
fn look_check_fails_on_stale_tokens() {
    let copy = copy_of_repository();
    let path = tokens_path(copy.path());
    let text = fs::read_to_string(&path).unwrap();
    fs::write(&path, text.replace("#0a0708", "#0a0709")).unwrap();
    let output = run(copy.path(), &["look", "--check"]);
    assert!(!output.status.success());
    assert!(said(&output).contains("tokens.css"), "{}", said(&output));
}

#[test]
fn look_check_fails_on_absent_tokens() {
    let copy = copy_of_repository();
    fs::remove_file(tokens_path(copy.path())).unwrap();
    let output = run(copy.path(), &["look", "--check"]);
    assert!(!output.status.success());
    assert!(said(&output).contains("tokens.css"), "{}", said(&output));
}

#[test]
fn look_check_passes_on_repository() {
    let output = run(&repository(), &["look", "--check"]);
    assert!(output.status.success(), "{}", said(&output));
}

#[test]
fn check_runs_the_look() {
    let copy = copy_of_repository();
    assert!(run(copy.path(), &["check"]).status.success());
    let path = tokens_path(copy.path());
    let text = fs::read_to_string(&path).unwrap();
    fs::write(&path, text.replace("#0a0708", "#0a0709")).unwrap();
    let output = run(copy.path(), &["check"]);
    assert!(!output.status.success());
    assert!(said(&output).contains("tokens.css"), "{}", said(&output));
}

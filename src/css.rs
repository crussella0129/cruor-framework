//! The stylesheet of the fonts, `fonts/fonts.css`: one `@font-face` rule for
//! each family and style, made from the list of families.

use std::fs;
use std::path::{Path, PathBuf};

use crate::families::{self, Family, STYLES};

/// The stylesheet, in the fonts' folder.
pub const STYLESHEET: &str = "fonts.css";

/// The stylesheet's path beneath a root.
pub fn path(root: &Path) -> PathBuf {
    families::fonts_dir(root).join(STYLESHEET)
}

/// The whole text of the stylesheet for a list of families.
///
/// The four styles of a family share the family's name and are told apart
/// by weight and slant, so a page that asks a family for its bold or its
/// italic is given that file. Each font is named by its bare file name: the
/// stylesheet works wherever it is served beside the fonts.
pub fn render(families: &[Family]) -> String {
    let mut css = String::from(
        "/*\n \
         * The faces of Cruor: each family under its own name, in four styles.\n \
         *\n \
         * This file is offered under MIT OR Apache-2.0. The fonts it names are\n \
         * offered under the SIL Open Font License 1.1; see OFL.txt beside it.\n \
         *\n \
         * It is made by the framework's tool from families.toml. Change the\n \
         * list and run `css`; do not change this file by hand.\n \
         */\n",
    );
    for family in families {
        css.push_str(&format!(
            "\n/* {}: {} */\n",
            family.name,
            family.kind.describes()
        ));
        for style in &STYLES {
            css.push_str(&format!(
                "@font-face {{\n  \
                 font-family: \"{}\";\n  \
                 font-style: {};\n  \
                 font-weight: {};\n  \
                 font-display: swap;\n  \
                 src: url(\"{}\") format(\"woff2\");\n\
                 }}\n",
                family.name,
                if style.italic { "italic" } else { "normal" },
                style.weight,
                family.file(style),
            ));
        }
    }
    css
}

/// What the stylesheet should hold, for the list beneath a root. Fails if
/// a font the list calls for is missing.
fn expected(root: &Path) -> Result<String, String> {
    let families = families::read(root)?;
    families::require_fonts(root, &families)?;
    Ok(render(&families))
}

/// Write the stylesheet beneath a root.
pub fn write(root: &Path) -> Result<(), String> {
    let css = expected(root)?;
    let path = path(root);
    fs::write(&path, css).map_err(|error| format!("cannot write {}: {error}", path.display()))
}

/// Fail if the stylesheet beneath a root is not what the list gives.
pub fn check(root: &Path) -> Result<(), String> {
    let css = expected(root)?;
    let path = path(root);
    let found =
        fs::read(&path).map_err(|error| format!("cannot read {}: {error}", path.display()))?;
    if found == css.as_bytes() {
        return Ok(());
    }
    Err(format!(
        "{} is not what {} gives; run `css` to write it again",
        path.display(),
        families::LIST
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    /// The list of families the repository holds.
    fn the_list() -> Vec<Family> {
        families::read(Path::new(env!("CARGO_MANIFEST_DIR"))).unwrap()
    }

    /// The declarations of every `@font-face` rule in a stylesheet.
    fn rules(css: &str) -> Vec<Vec<(String, String)>> {
        css.split("@font-face {")
            .skip(1)
            .map(|rest| {
                let body = rest.split('}').next().unwrap();
                body.split(';')
                    .filter_map(|declaration| declaration.trim().split_once(':'))
                    .map(|(property, value)| {
                        (property.trim().to_string(), value.trim().to_string())
                    })
                    .collect()
            })
            .collect()
    }

    fn value<'a>(rule: &'a [(String, String)], property: &str) -> &'a str {
        let found: Vec<_> = rule.iter().filter(|(p, _)| p == property).collect();
        assert_eq!(found.len(), 1, "one `{property}` in {rule:?}");
        &found[0].1
    }

    #[test]
    fn css_has_thirty_two_rules() {
        let rules = rules(&render(&the_list()));
        assert_eq!(rules.len(), 32);
        for (index, rule) in rules.iter().enumerate() {
            assert!(
                !rules[..index].contains(rule),
                "no two rules alike: {rule:?}"
            );
        }
    }

    #[test]
    fn css_rule_descriptors_match_style() {
        let list = the_list();
        assert_eq!(list.len(), 8);
        let rules = rules(&render(&list));
        let mut rule = rules.iter();
        for family in &list {
            for style in &STYLES {
                let rule = rule.next().unwrap();
                assert_eq!(rule.len(), 5, "five declarations in {rule:?}");
                assert_eq!(value(rule, "font-family"), format!("\"{}\"", family.name));
                assert_eq!(
                    value(rule, "font-weight"),
                    if style.suffix.starts_with("Bold") {
                        "700"
                    } else {
                        "400"
                    }
                );
                assert_eq!(
                    value(rule, "font-style"),
                    if style.suffix.ends_with("Italic") {
                        "italic"
                    } else {
                        "normal"
                    }
                );
                assert_eq!(
                    value(rule, "src"),
                    format!(
                        "url(\"{}-{}.woff2\") format(\"woff2\")",
                        family.stem, style.suffix
                    )
                );
                assert_eq!(value(rule, "font-display"), "swap");
            }
        }
    }

    #[test]
    fn css_comment_states_both_terms() {
        let css = render(&the_list());
        assert!(css.starts_with("/*"));
        let comment = &css[..css.find("*/").unwrap()];
        assert!(comment.contains("This file is offered under MIT OR Apache-2.0"));
        assert!(
            comment.contains("fonts it names are\n * offered under the SIL Open Font License 1.1")
        );
        assert!(comment.contains("made by the framework's tool"));
    }
}

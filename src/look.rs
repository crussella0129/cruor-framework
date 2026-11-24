//! The tokens of the look, `look/tokens.css`: one custom property for each
//! thing the theme file says, made from the theme file.
//!
//! The look's stylesheets name every colour, family and measure by one of
//! these, and never write one out. So a look is changed in the theme file
//! and nowhere else.

use std::fs;
use std::path::{Path, PathBuf};

use crate::contrast;
use crate::theme::{self, Theme};

/// The tokens' stylesheet, in the look's folder.
pub const TOKENS: &str = "tokens.css";

/// The tokens' path beneath a root.
pub fn path(root: &Path) -> PathBuf {
    theme::look_dir(root).join(TOKENS)
}

/// A family's name as a stylesheet writes it.
fn quoted(family: &str) -> String {
    format!("\"{family}\"")
}

/// Every token and its value, in the order the theme file gives them.
///
/// A token is named for where its value stands in the theme file: a colour
/// role by its name, a role of the void or a key of the stone with that
/// table's name before it, a font role after `font-`, a measure by its
/// name, and a heading's five settings after its level.
pub fn tokens(theme: &Theme) -> Vec<(String, String)> {
    let mut all = Vec::new();
    for (role, colour) in &theme.colours {
        all.push((role.to_string(), colour.written().to_string()));
    }
    for (role, colour) in &theme.void {
        all.push((format!("void-{role}"), colour.written().to_string()));
    }
    all.push(("stone-sheen".into(), theme.sheen.written().to_string()));
    all.push((
        "stone-sheen-opacity".into(),
        theme.sheen_opacity.to_string(),
    ));
    all.push(("stone-candle".into(), theme.candle.written().to_string()));
    all.push((
        "stone-candle-opacity".into(),
        theme.candle_opacity.to_string(),
    ));
    for (role, family) in &theme.fonts {
        all.push((format!("font-{role}"), quoted(family)));
    }
    all.push(("inscription-size".into(), theme.inscription_size.clone()));
    all.push(("interface-size".into(), theme.interface_size.clone()));
    all.push(("line".into(), theme.line.to_string()));
    all.push(("column".into(), theme.column.clone()));
    all.push(("seal-size".into(), theme.seal_size.to_string()));
    all.push(("seal-font".into(), quoted(&theme.seal_family)));
    for heading in &theme.headings {
        let level = heading.level;
        all.push((format!("{level}-font"), quoted(&heading.family)));
        let weight = if heading.bold { "700" } else { "400" };
        all.push((format!("{level}-weight"), weight.into()));
        let style = if heading.italic { "italic" } else { "normal" };
        all.push((format!("{level}-style"), style.into()));
        let line = if heading.underline {
            "underline"
        } else {
            "none"
        };
        all.push((format!("{level}-decoration"), line.into()));
        all.push((format!("{level}-size"), heading.size.clone()));
    }
    all
}

/// The whole text of the tokens' stylesheet for a theme: one rule, on the
/// look's class, holding the tokens and nothing else.
pub fn render(theme: &Theme) -> String {
    let mut css = format!(
        "/*\n \
         * The tokens of {}: its colours, its families and its measures.\n \
         *\n \
         * This file is offered under MIT OR Apache-2.0.\n \
         *\n \
         * It is made by the framework's tool from theme.toml. Change the theme\n \
         * file and run `look`; do not change this file by hand.\n \
         */\n\n\
         .{} {{\n",
        theme.name, theme.class
    );
    for (name, value) in tokens(theme) {
        css.push_str(&format!("  --cruor-{name}: {value};\n"));
    }
    css.push_str("}\n");
    css
}

/// What the tokens should hold, for the theme beneath a root. Fails if the
/// theme file is not as its form requires, or does not keep the contrast it
/// promises.
fn expected(root: &Path) -> Result<String, String> {
    let theme = theme::read(root)?;
    contrast::check(&theme)
        .map_err(|faults| format!("{}/{}: {faults}", theme::LOOK_DIR, theme::THEME))?;
    Ok(render(&theme))
}

/// Write the tokens beneath a root from the theme file there.
pub fn write(root: &Path) -> Result<(), String> {
    let css = expected(root)?;
    let path = path(root);
    fs::write(&path, css).map_err(|error| format!("cannot write {}: {error}", path.display()))
}

/// Fail if the theme file beneath a root is not as its form requires, does
/// not keep the contrast it promises, or if the tokens there are not what it
/// gives.
pub fn check(root: &Path) -> Result<(), String> {
    let css = expected(root)?;
    let path = path(root);
    let found =
        fs::read(&path).map_err(|error| format!("cannot read {}: {error}", path.display()))?;
    if found == css.as_bytes() {
        return Ok(());
    }
    Err(format!(
        "{} is not what {} gives; run `look` to write it again",
        path.display(),
        theme::THEME
    ))
}

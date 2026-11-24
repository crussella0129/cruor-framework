//! The theme file, `look/theme.toml`: the look written down once, by role.
//!
//! This is the one reader of the file. It takes the file's form strictly: a
//! key the form requires must be there, and a key the form does not have
//! must not be, so that a slip in a name is told and not passed over. Every
//! fault names its key as it is written in the file, table and all.

use std::fs;
use std::path::{Path, PathBuf};

use crate::families;

/// The folder, beneath the repository's root, that holds the look.
pub const LOOK_DIR: &str = "look";

/// The theme file, in the look's folder.
pub const THEME: &str = "theme.toml";

/// What a family is set for. A heading names one of these, or a family.
pub const FONT_ROLES: [&str; 4] = ["title", "heading", "text", "code"];

/// The colours of the look, by role, in the order they are always given.
pub const COLOUR_ROLES: [&str; 22] = [
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

/// The colours of the void, by role.
pub const VOID_ROLES: [&str; 8] = [
    "ground",
    "sunken",
    "row",
    "text",
    "text-subdued",
    "accent",
    "channel",
    "border",
];

/// The heading levels.
pub const LEVELS: [&str; 6] = ["h1", "h2", "h3", "h4", "h5", "h6"];

/// A colour as the theme file writes it: `#rrggbb`, or `rgba(r, g, b, a)`.
#[derive(Debug, Clone, PartialEq)]
pub struct Colour {
    pub red: u8,
    pub green: u8,
    pub blue: u8,
    /// How much of what lies beneath it shows through: 1 is none.
    pub alpha: f64,
    written: String,
}

impl Colour {
    /// Read a colour, or say nothing if it is not one.
    pub fn parse(text: &str) -> Option<Colour> {
        let written = text.to_string();
        if let Some(hex) = text.strip_prefix('#') {
            if hex.len() != 6 || !hex.bytes().all(|byte| byte.is_ascii_hexdigit()) {
                return None;
            }
            let channel = |at: usize| u8::from_str_radix(&hex[at..at + 2], 16).ok();
            return Some(Colour {
                red: channel(0)?,
                green: channel(2)?,
                blue: channel(4)?,
                alpha: 1.0,
                written,
            });
        }
        let inner = text.strip_prefix("rgba(")?.strip_suffix(')')?;
        let parts: Vec<&str> = inner.split(',').map(str::trim).collect();
        if parts.len() != 4 {
            return None;
        }
        let alpha: f64 = parts[3].parse().ok()?;
        if !(0.0..=1.0).contains(&alpha) {
            return None;
        }
        Some(Colour {
            red: parts[0].parse().ok()?,
            green: parts[1].parse().ok()?,
            blue: parts[2].parse().ok()?,
            alpha,
            written,
        })
    }

    /// The colour as the theme file wrote it, which is how a stylesheet
    /// writes it too.
    #[allow(dead_code)]
    pub fn written(&self) -> &str {
        &self.written
    }
}

/// One heading level, as the theme file sets it.
#[allow(dead_code)]
#[derive(Debug, Clone, PartialEq)]
pub struct Heading {
    pub level: &'static str,
    /// The family it is set in, whichever way the file named it.
    pub family: String,
    pub bold: bool,
    pub italic: bool,
    pub underline: bool,
    pub size: String,
}

/// The look, as the theme file gives it.
// Read by `look` when it writes the tokens; until then only judged.
#[allow(dead_code)]
#[derive(Debug, Clone, PartialEq)]
pub struct Theme {
    pub name: String,
    /// The class a page sets to take the look on.
    pub class: String,
    /// The family of each font role.
    pub fonts: Vec<(&'static str, String)>,
    pub colours: Vec<(&'static str, Colour)>,
    pub void: Vec<(&'static str, Colour)>,
    /// The stone's brightest tone, and how strongly it is laid on the page.
    pub sheen: Colour,
    pub sheen_opacity: f64,
    /// The glow from above, and its strength at its strongest.
    pub candle: Colour,
    pub candle_opacity: f64,
    pub inscription_size: String,
    pub interface_size: String,
    pub line: f64,
    pub column: String,
    pub seal_size: f64,
    /// The family of the large first letter.
    pub seal_family: String,
    pub headings: Vec<Heading>,
}

/// The look's folder beneath a root.
pub fn look_dir(root: &Path) -> PathBuf {
    root.join(LOOK_DIR)
}

/// Read the theme file beneath a root.
pub fn read(root: &Path) -> Result<Theme, String> {
    let path = look_dir(root).join(THEME);
    let text = fs::read_to_string(&path)
        .map_err(|error| format!("cannot read {}: {error}", path.display()))?;
    let kit: Vec<String> = families::read(root)?
        .into_iter()
        .map(|family| family.name)
        .collect();
    parse(&text, &kit).map_err(|error| format!("{LOOK_DIR}/{THEME}: {error}"))
}

/// One table of the file, from which each key is taken once. What is left
/// when the form has taken all it knows is a key the form does not have.
struct Section {
    /// How the table is written in a key's name: empty at the top, else
    /// `colour.` and the like.
    prefix: String,
    table: toml::Table,
}

impl Section {
    fn name(&self, key: &str) -> String {
        format!("{}{key}", self.prefix)
    }

    fn take(&mut self, key: &str) -> Result<toml::Value, String> {
        self.table
            .remove(key)
            .ok_or_else(|| format!("{}: missing", self.name(key)))
    }

    fn string(&mut self, key: &str) -> Result<String, String> {
        match self.take(key)? {
            toml::Value::String(text) => Ok(text),
            _ => Err(format!("{}: not a string", self.name(key))),
        }
    }

    fn number(&mut self, key: &str) -> Result<f64, String> {
        match self.take(key)? {
            toml::Value::Float(number) => Ok(number),
            toml::Value::Integer(number) => Ok(number as f64),
            _ => Err(format!("{}: not a number", self.name(key))),
        }
    }

    fn truth(&mut self, key: &str) -> Result<bool, String> {
        match self.take(key)? {
            toml::Value::Boolean(truth) => Ok(truth),
            _ => Err(format!("{}: not true or false", self.name(key))),
        }
    }

    fn colour(&mut self, key: &str) -> Result<Colour, String> {
        let text = self.string(key)?;
        Colour::parse(&text).ok_or_else(|| {
            format!(
                "{}: {text:?} is not a colour; write #rrggbb or rgba(r, g, b, a)",
                self.name(key)
            )
        })
    }

    /// A share between nothing and all: 0 to 1.
    fn share(&mut self, key: &str) -> Result<f64, String> {
        let number = self.number(key)?;
        if (0.0..=1.0).contains(&number) {
            Ok(number)
        } else {
            Err(format!("{}: not between 0 and 1", self.name(key)))
        }
    }

    /// A length a stylesheet can take: a number and `rem`, `em` or `px`.
    fn length(&mut self, key: &str) -> Result<String, String> {
        let text = self.string(key)?;
        let number = ["rem", "em", "px"]
            .iter()
            .find_map(|unit| text.strip_suffix(unit));
        match number {
            Some(digits) if digits.parse::<f64>().is_ok_and(|value| value > 0.0) => Ok(text),
            _ => Err(format!(
                "{}: {text:?} is not a length; write a number and rem, em or px",
                self.name(key)
            )),
        }
    }

    fn section(&mut self, key: &str) -> Result<Section, String> {
        match self.take(key)? {
            toml::Value::Table(table) => Ok(Section {
                prefix: format!("{}.", self.name(key)),
                table,
            }),
            _ => Err(format!("{}: not a table", self.name(key))),
        }
    }

    /// Finish with the table: a key still in it is one the form has not.
    fn done(self) -> Result<(), String> {
        match self.table.keys().next() {
            None => Ok(()),
            Some(key) => Err(format!("{}: the form has no such key", self.name(key))),
        }
    }
}

/// The family a heading or the seal is set in: one of the four roles gives
/// that role's family; else the name must be a family the kit holds.
fn family_of(
    named: &str,
    key: &str,
    fonts: &[(&'static str, String)],
    kit: &[String],
) -> Result<String, String> {
    if let Some((_, family)) = fonts.iter().find(|(role, _)| *role == named) {
        return Ok(family.clone());
    }
    if kit.iter().any(|family| family == named) {
        return Ok(named.to_string());
    }
    Err(format!(
        "{key}: {named:?} is neither one of the four font roles nor a family the kit holds"
    ))
}

/// Read a theme from its text. `kit` is the names of the families the kit
/// holds, as `fonts/families.toml` lists them.
pub fn parse(text: &str, kit: &[String]) -> Result<Theme, String> {
    let table: toml::Table = text
        .parse()
        .map_err(|error: toml::de::Error| error.to_string())?;
    let mut top = Section {
        prefix: String::new(),
        table,
    };

    let name = top.string("name")?;
    let class = top.string("class")?;
    let fits = !class.is_empty()
        && class
            .bytes()
            .all(|byte| byte.is_ascii_lowercase() || byte.is_ascii_digit() || byte == b'-')
        && !class.starts_with(|first: char| first.is_ascii_digit() || first == '-');
    if !fits {
        return Err(format!(
            "class: {class:?} cannot be a class; write small letters, digits and hyphens"
        ));
    }

    let mut section = top.section("font")?;
    let mut fonts = Vec::new();
    for role in FONT_ROLES {
        let family = section.string(role)?;
        if !kit.contains(&family) {
            return Err(format!(
                "font.{role}: the kit holds no family named {family:?}"
            ));
        }
        fonts.push((role, family));
    }
    section.done()?;

    let mut section = top.section("colour")?;
    let mut colours = Vec::new();
    for role in COLOUR_ROLES {
        colours.push((role, section.colour(role)?));
    }
    section.done()?;

    let mut section = top.section("void")?;
    let mut void = Vec::new();
    for role in VOID_ROLES {
        void.push((role, section.colour(role)?));
    }
    section.done()?;

    let mut section = top.section("stone")?;
    let sheen = section.colour("sheen")?;
    let sheen_opacity = section.share("sheen-opacity")?;
    let candle = section.colour("candle")?;
    let candle_opacity = section.share("candle-opacity")?;
    section.done()?;

    let mut section = top.section("measure")?;
    let inscription_size = section.length("inscription-size")?;
    let interface_size = section.length("interface-size")?;
    let line = section.number("line")?;
    let column = section.length("column")?;
    let seal_size = section.number("seal-size")?;
    let seal_font = section.string("seal-font")?;
    let seal_family = family_of(&seal_font, "measure.seal-font", &fonts, kit)?;
    section.done()?;

    let mut levels = top.section("heading")?;
    let mut headings = Vec::new();
    for level in LEVELS {
        let mut section = levels.section(level)?;
        let font = section.string("font")?;
        let family = family_of(&font, &format!("heading.{level}.font"), &fonts, kit)?;
        headings.push(Heading {
            level,
            family,
            bold: section.truth("bold")?,
            italic: section.truth("italic")?,
            underline: section.truth("underline")?,
            size: section.length("size")?,
        });
        section.done()?;
    }
    levels.done()?;
    top.done()?;

    Ok(Theme {
        name,
        class,
        fonts,
        colours,
        void,
        sheen,
        sheen_opacity,
        candle,
        candle_opacity,
        inscription_size,
        interface_size,
        line,
        column,
        seal_size,
        seal_family,
        headings,
    })
}

#[cfg(test)]
mod tests {
    use super::Colour;

    #[test]
    fn colour_reads_both_forms() {
        let solid = Colour::parse("#0a0708").unwrap();
        assert_eq!((solid.red, solid.green, solid.blue), (10, 7, 8));
        assert_eq!(solid.alpha, 1.0);
        let clear = Colour::parse("rgba(213, 2, 16, 0.2)").unwrap();
        assert_eq!((clear.red, clear.green, clear.blue), (213, 2, 16));
        assert_eq!(clear.alpha, 0.2);
        assert_eq!(clear.written(), "rgba(213, 2, 16, 0.2)");
    }

    #[test]
    fn colour_refuses_what_is_not_one() {
        for text in [
            "#12",
            "#12345g",
            "red",
            "rgba(1, 2, 3)",
            "rgba(1, 2, 3, 2)",
            "rgb(1, 2, 3)",
        ] {
            assert!(Colour::parse(text).is_none(), "{text}");
        }
    }
}

//! The list of families, `fonts/families.toml`, and what follows from it:
//! which font files there must be, and what each one is.
//!
//! This is the one reader of the list. Every command starts here.

use std::fs;
use std::path::{Path, PathBuf};

use serde::Deserialize;

/// The folder, beneath the repository's root, that holds the fonts, their
/// stylesheet and their licence: one flat folder, as a release is.
pub const FONTS_DIR: &str = "fonts";

/// The list of families, in the fonts' folder.
pub const LIST: &str = "families.toml";

/// How a family's characters are set.
#[derive(Debug, Clone, Copy, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum Kind {
    Proportional,
    Mono,
    Pixel,
}

impl Kind {
    /// What the kind means, in a few words.
    pub fn describes(self) -> &'static str {
        match self {
            Kind::Proportional => "each letter at a width of its own",
            Kind::Mono => "every character in one cell",
            Kind::Pixel => "every character in one cell, on a lattice of squares",
        }
    }
}

/// One family of Cruor, as the list gives it.
#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct Family {
    /// The family's name, exactly as its fonts give it.
    pub name: String,
    /// What its files' names begin with.
    pub stem: String,
    pub kind: Kind,
}

impl Family {
    /// The name of the file that holds one style of this family.
    pub fn file(&self, style: &Style) -> String {
        format!("{}-{}.woff2", self.stem, style.suffix)
    }
}

/// One of the four styles every family has.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Style {
    /// How the style is written in a file's name.
    pub suffix: &'static str,
    /// The weight a page asks for: 400 or 700.
    pub weight: u16,
    pub italic: bool,
}

/// The four styles, in the order they are always given.
pub const STYLES: [Style; 4] = [
    Style {
        suffix: "Regular",
        weight: 400,
        italic: false,
    },
    Style {
        suffix: "Bold",
        weight: 700,
        italic: false,
    },
    Style {
        suffix: "Italic",
        weight: 400,
        italic: true,
    },
    Style {
        suffix: "BoldItalic",
        weight: 700,
        italic: true,
    },
];

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct List {
    family: Vec<Family>,
}

/// The fonts' folder beneath a root.
pub fn fonts_dir(root: &Path) -> PathBuf {
    root.join(FONTS_DIR)
}

/// Read the list of families beneath a root.
pub fn read(root: &Path) -> Result<Vec<Family>, String> {
    let path = fonts_dir(root).join(LIST);
    let text = fs::read_to_string(&path)
        .map_err(|error| format!("cannot read {}: {error}", path.display()))?;
    parse(&text).map_err(|error| format!("{}: {error}", path.display()))
}

/// Read a list of families from its text.
pub fn parse(text: &str) -> Result<Vec<Family>, String> {
    let list: List = toml::from_str(text).map_err(|error| error.to_string())?;
    if list.family.is_empty() {
        return Err("the list names no family".to_string());
    }
    for (index, family) in list.family.iter().enumerate() {
        let earlier = &list.family[..index];
        if earlier.iter().any(|other| other.name == family.name) {
            return Err(format!("the family {:?} is listed twice", family.name));
        }
        if earlier.iter().any(|other| other.stem == family.stem) {
            return Err(format!("the stem {:?} is listed twice", family.stem));
        }
        let plain = |c: char| c.is_ascii_alphanumeric();
        if family.stem.is_empty() || !family.stem.chars().all(plain) {
            return Err(format!(
                "the stem {:?} must be letters and figures alone",
                family.stem
            ));
        }
        if family.name.is_empty() || family.name.contains(['"', '\\', '\n']) {
            return Err(format!(
                "the name {:?} cannot be written in a rule",
                family.name
            ));
        }
    }
    Ok(list.family)
}

/// The name of every font file the list calls for, family by family and
/// style by style.
pub fn font_files(families: &[Family]) -> Vec<String> {
    families
        .iter()
        .flat_map(|family| STYLES.iter().map(|style| family.file(style)))
        .collect()
}

/// The font files the list calls for that are not in the fonts' folder.
pub fn missing_fonts(root: &Path, families: &[Family]) -> Vec<String> {
    let folder = fonts_dir(root);
    font_files(families)
        .into_iter()
        .filter(|name| !folder.join(name).is_file())
        .collect()
}

/// Fail, naming them, if any font the list calls for is missing.
pub fn require_fonts(root: &Path, families: &[Family]) -> Result<(), String> {
    let missing = missing_fonts(root, families);
    if missing.is_empty() {
        return Ok(());
    }
    Err(format!(
        "{} called for by {} but not in {}: {}",
        if missing.len() == 1 {
            "a font is"
        } else {
            "fonts are"
        },
        LIST,
        fonts_dir(root).display(),
        missing.join(", ")
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn a_list_gives_four_files_a_family() {
        let families = parse(
            "[[family]]\nname = \"Cruor Sans Mono\"\nstem = \"CruorSansMono\"\nkind = \"mono\"\n",
        )
        .unwrap();
        assert_eq!(
            font_files(&families),
            [
                "CruorSansMono-Regular.woff2",
                "CruorSansMono-Bold.woff2",
                "CruorSansMono-Italic.woff2",
                "CruorSansMono-BoldItalic.woff2",
            ]
        );
    }

    #[test]
    fn a_list_is_refused_for_what_would_break_a_rule_or_a_file_name() {
        let with = |name: &str, stem: &str, kind: &str| {
            parse(&format!(
                "[[family]]\nname = '{name}'\nstem = '{stem}'\nkind = '{kind}'\n"
            ))
        };
        assert!(with("Cruor Sans Mono", "CruorSansMono", "mono").is_ok());
        assert!(with("Cruor Sans Mono", "Cruor/SansMono", "mono").is_err());
        assert!(with("Cruor \"Sans\" Mono", "CruorSansMono", "mono").is_err());
        assert!(with("Cruor Sans Mono", "CruorSansMono", "wide").is_err());
        assert!(parse("").is_err());
        let twice = "[[family]]\nname = 'A'\nstem = 'A'\nkind = 'mono'\n".repeat(2);
        assert!(parse(&twice).is_err());
    }
}

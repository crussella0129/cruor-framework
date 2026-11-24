//! The contrast the theme file promises, and the test of it.
//!
//! The theme file says which text may sit on which ground, and at what
//! ratio at least. Those promises are kept here, from the file's own
//! colours, so a look whose text cannot be read is refused before a single
//! token is written.
//!
//! The ratio is WCAG 2's, from relative luminance. It is compared with the
//! bound as it is found, without rounding.

use crate::theme::{Colour, Theme};

/// A colour with nothing showing through it: red, green and blue, each from
/// 0 to 255, and not always whole, since one colour laid over another at a
/// share falls between the steps.
pub type Solid = [f64; 3];

/// One colour laid over another at a share of its strength.
pub fn over(top: Solid, share: f64, under: Solid) -> Solid {
    [0, 1, 2].map(|at| top[at] * share + under[at] * (1.0 - share))
}

/// A theme's colour laid over a ground: itself, if nothing shows through it.
pub fn laid(colour: &Colour, under: Solid) -> Solid {
    let top = [
        f64::from(colour.red),
        f64::from(colour.green),
        f64::from(colour.blue),
    ];
    over(top, colour.alpha, under)
}

/// How bright a colour is to the eye, from 0 to 1.
pub fn luminance(colour: Solid) -> f64 {
    let linear = |channel: f64| {
        let share = channel / 255.0;
        if share <= 0.03928 {
            share / 12.92
        } else {
            ((share + 0.055) / 1.055).powf(2.4)
        }
    };
    0.2126 * linear(colour[0]) + 0.7152 * linear(colour[1]) + 0.0722 * linear(colour[2])
}

/// The ratio between two colours, from 1 to 21.
pub fn ratio(one: Solid, other: Solid) -> f64 {
    let (one, other) = (luminance(one), luminance(other));
    (one.max(other) + 0.05) / (one.min(other) + 0.05)
}

fn role<'a>(colours: &'a [(&'static str, Colour)], name: &str) -> Option<&'a Colour> {
    colours
        .iter()
        .find(|(role, _)| *role == name)
        .map(|(_, colour)| colour)
}

/// The page's own ground.
fn page(theme: &Theme) -> Solid {
    let colour = role(&theme.colours, "page").expect("the form requires a page");
    laid(colour, [0.0, 0.0, 0.0])
}

/// The page at its brightest: the stone's sheen laid over the page at its
/// opacity, and then the candle's glow laid over that at its own.
pub fn stone(theme: &Theme) -> Solid {
    let sheen = laid(&theme.sheen, page(theme));
    let lit = over(sheen, theme.sheen_opacity, page(theme));
    let candle = laid(&theme.candle, lit);
    over(candle, theme.candle_opacity, lit)
}

/// A ground, by the name a promise gives it.
///
/// `stone` is the page at its brightest. A colour role is that colour, laid
/// over the page if anything shows through it. `void.` and a role of the
/// void is that colour, laid over the void's own ground; `void.row` and
/// `void.sunken-row` are the tint of the current row over the void's ground
/// and over its sunken one.
pub fn ground(theme: &Theme, name: &str) -> Option<Solid> {
    if name == "stone" {
        return Some(stone(theme));
    }
    let Some(within) = name.strip_prefix("void.") else {
        return role(&theme.colours, name).map(|colour| laid(colour, page(theme)));
    };
    let floor = laid(role(&theme.void, "ground")?, [0.0, 0.0, 0.0]);
    match within {
        "row" => Some(laid(role(&theme.void, "row")?, floor)),
        "sunken-row" => {
            let sunken = laid(role(&theme.void, "sunken")?, floor);
            Some(laid(role(&theme.void, "row")?, sunken))
        }
        _ => role(&theme.void, within).map(|colour| laid(colour, floor)),
    }
}

/// A text role's colour, by the name a promise gives it: a colour role, or
/// `void.` and a role of the void.
pub fn text<'a>(theme: &'a Theme, name: &str) -> Option<&'a Colour> {
    match name.strip_prefix("void.") {
        Some(within) => role(&theme.void, within),
        None => role(&theme.colours, name),
    }
}

/// Hold a theme to every promise it makes. Says everything that falls
/// short, not the first thing.
pub fn check(theme: &Theme) -> Result<(), String> {
    let mut faults = Vec::new();
    for (index, promise) in theme.contrast.iter().enumerate() {
        let at = index + 1;
        for ground_name in &promise.grounds {
            let Some(under) = ground(theme, ground_name) else {
                faults.push(format!(
                    "contrast entry {at}: {ground_name:?} is no ground of the theme"
                ));
                continue;
            };
            for text_name in &promise.text {
                let Some(colour) = text(theme, text_name) else {
                    faults.push(format!(
                        "contrast entry {at}: {text_name:?} is no text role of the theme"
                    ));
                    continue;
                };
                let found = ratio(laid(colour, under), under);
                if found < promise.at_least {
                    faults.push(format!(
                        "contrast: {text_name} on {ground_name} stands at {found:.2}, \
                         and {} is promised",
                        promise.at_least
                    ));
                }
            }
        }
    }
    faults.dedup();
    if faults.is_empty() {
        Ok(())
    } else {
        Err(faults.join("\n  "))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::theme;
    use std::path::Path;

    fn the_look() -> Theme {
        theme::read(Path::new(env!("CARGO_MANIFEST_DIR"))).unwrap()
    }

    fn near(one: f64, other: f64, places: i32) -> bool {
        (one - other).abs() < 0.5 * 10f64.powi(-places)
    }

    #[test]
    fn ratio_is_wcags() {
        let (black, white) = ([0.0; 3], [255.0; 3]);
        assert!(near(ratio(black, white), 21.0, 6));
        assert!(near(ratio([119.0; 3], white), 4.48, 2));
        assert_eq!(ratio(white, black), ratio(black, white));
    }

    #[test]
    fn contrast_lays_the_sheen_then_the_candle() {
        // Worked by hand from the theme as written: the page is 10, 7, 8;
        // the sheen 58, 42, 44 laid over it at 0.3 gives 24.4, 17.5, 18.8;
        // the candle 255, 60, 40 laid over that at 0.03 gives the stone.
        let look = the_look();
        let stone = stone(&look);
        for (found, worked) in stone.iter().zip([31.318, 18.775, 19.436]) {
            assert!(near(*found, worked, 4), "{found} against {worked}");
        }
        // The other order would give another colour.
        let page = [10.0, 7.0, 8.0];
        let candle_first = over(
            [58.0, 42.0, 44.0],
            0.3,
            over([255.0, 60.0, 40.0], 0.03, page),
        );
        assert!(!near(candle_first[0], stone[0], 1));

        // The inscription on it, which is the look's narrowest promise.
        let inscription = text(&look, "inscription").unwrap();
        assert!(near(ratio(laid(inscription, stone), stone), 3.31, 2));
    }

    #[test]
    fn contrast_does_not_round() {
        // A bound one part in a thousand above the ratio found is not met,
        // though the two agree to two places.
        let mut look = the_look();
        let stone = stone(&look);
        let inscription = text(&look, "inscription").unwrap();
        let found = ratio(laid(inscription, stone), stone);
        look.contrast = vec![theme::Promise {
            text: vec!["inscription".into()],
            grounds: vec!["stone".into()],
            at_least: found + 0.001,
        }];
        assert!(check(&look).is_err());
        look.contrast[0].at_least = found;
        assert!(check(&look).is_ok());
    }
}

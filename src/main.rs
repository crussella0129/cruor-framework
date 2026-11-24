//! The tool of the Cruor framework.
//!
//! It writes the stylesheet of Cruor's web fonts from the list of families,
//! writes and checks the manifest of their checksums, writes the look's
//! tokens from its theme file, and puts a release together.

mod bundle;
mod contrast;
mod css;
mod families;
mod look;
mod manifest;
mod theme;

use std::path::{Path, PathBuf};
use std::process::ExitCode;

use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(
    name = "cruor-framework",
    version,
    about = "Writes the stylesheet of Cruor's web fonts, their manifest, and a release"
)]
struct Cli {
    /// The repository's root, if it is not the folder this is run from
    #[arg(long, global = true, value_name = "DIR", default_value = ".")]
    root: PathBuf,

    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand)]
enum Command {
    /// Write fonts/fonts.css from the list of families
    Css {
        /// Change nothing; fail if the stylesheet is not what the list gives
        #[arg(long)]
        check: bool,
    },
    /// Write fonts/manifest.toml: each font's size and SHA-256
    Manifest {
        /// Change nothing; fail if a font and the manifest disagree
        #[arg(long, conflicts_with = "source_commit")]
        check: bool,

        /// The commit of the Cruor project the fonts were built at, in full
        #[arg(long, value_name = "ID")]
        source_commit: Option<String>,
    },
    /// Write look/tokens.css from the look's theme file, look/theme.toml
    Look {
        /// Change nothing; fail if the theme file is not as its form requires,
        /// or if the tokens are not what it gives
        #[arg(long)]
        check: bool,
    },
    /// Check that the stylesheet, the manifest and the look's tokens are current
    Check,
    /// Put a release together in a folder
    Bundle {
        /// The folder to put it in; it must be absent or empty
        #[arg(long, value_name = "DIR")]
        out: PathBuf,

        /// Fail unless this is the tag of the framework's version: `v`, then the version
        #[arg(long, value_name = "TAG")]
        tag: Option<String>,
    },
}

fn run(cli: &Cli) -> Result<(), String> {
    match &cli.command {
        Command::Css { check: true } => css::check(&cli.root),
        Command::Css { check: false } => css::write(&cli.root),
        Command::Manifest { check: true, .. } => manifest::check(&cli.root),
        Command::Manifest {
            check: false,
            source_commit,
        } => manifest::write(&cli.root, source_commit.as_deref()),
        Command::Look { check: true } => look::check(&cli.root),
        Command::Look { check: false } => look::write(&cli.root),
        Command::Check => check(&cli.root),
        Command::Bundle { out, tag } => bundle::bundle(&cli.root, out, tag.as_deref()),
    }
}

/// Run every check, and say everything that is wrong, not the first thing.
fn check(root: &Path) -> Result<(), String> {
    let faults: Vec<String> = [css::check(root), manifest::check(root), look::check(root)]
        .into_iter()
        .filter_map(Result::err)
        .collect();
    if faults.is_empty() {
        Ok(())
    } else {
        Err(faults.join("\ncruor-framework: "))
    }
}

fn main() -> ExitCode {
    let cli = Cli::parse();
    match run(&cli) {
        Ok(()) => ExitCode::SUCCESS,
        Err(message) => {
            eprintln!("cruor-framework: {message}");
            ExitCode::FAILURE
        }
    }
}

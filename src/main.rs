//! The tool of the Cruor framework.
//!
//! It writes the stylesheet of Cruor's web fonts from the list of families,
//! writes and checks the manifest of their checksums, and puts a release
//! together. Each command is built by its own task; until then it says so.

mod css;
mod families;
mod manifest;

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
    /// Check that the stylesheet and the manifest are current
    Check,
    /// Put a release together in a folder
    Bundle,
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
        Command::Check => check(&cli.root),
        Command::Bundle => Err("`bundle` is not built yet".to_string()),
    }
}

/// Run both checks, and say everything that is wrong, not the first thing.
fn check(root: &Path) -> Result<(), String> {
    let faults: Vec<String> = [css::check(root), manifest::check(root)]
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

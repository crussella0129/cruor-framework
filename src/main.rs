//! The tool of the Cruor framework.
//!
//! It writes the stylesheet of Cruor's web fonts from the list of families,
//! writes and checks the manifest of their checksums, and puts a release
//! together. Each command is built by its own task; until then it says so.

mod css;
mod families;

use std::path::PathBuf;
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
    Manifest,
    /// Check that the stylesheet and the manifest are current
    Check,
    /// Put a release together in a folder
    Bundle,
}

fn run(cli: &Cli) -> Result<(), String> {
    match &cli.command {
        Command::Css { check: true } => css::check(&cli.root),
        Command::Css { check: false } => css::write(&cli.root),
        Command::Manifest => Err("`manifest` is not built yet".to_string()),
        Command::Check => Err("`check` is not built yet".to_string()),
        Command::Bundle => Err("`bundle` is not built yet".to_string()),
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

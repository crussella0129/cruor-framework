//! The tool of the Cruor framework.
//!
//! It writes the stylesheet of Cruor's web fonts from the list of families,
//! writes and checks the manifest of their checksums, and puts a release
//! together. Each command is built by its own task; until then it says so.

use std::process::ExitCode;

use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(
    name = "cruor-framework",
    version,
    about = "Writes the stylesheet of Cruor's web fonts, their manifest, and a release"
)]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand)]
enum Command {
    /// Write fonts/fonts.css from the list of families
    Css,
    /// Write fonts/manifest.toml: each font's size and SHA-256
    Manifest,
    /// Check that the stylesheet and the manifest are current
    Check,
    /// Put a release together in a folder
    Bundle,
}

impl Command {
    fn name(&self) -> &'static str {
        match self {
            Command::Css => "css",
            Command::Manifest => "manifest",
            Command::Check => "check",
            Command::Bundle => "bundle",
        }
    }
}

fn main() -> ExitCode {
    let cli = Cli::parse();
    eprintln!("cruor-framework: `{}` is not built yet", cli.command.name());
    ExitCode::from(2)
}

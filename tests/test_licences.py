"""The terms the code is offered under: both licences, and the crate's word."""

import hashlib
import tomllib

from helpers import ROOT

# The Apache License 2.0 as its authors publish it, byte for byte.
APACHE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"


def test_code_licences_present():
    mit = (ROOT / "LICENSE-MIT").read_text(encoding="utf-8")
    assert "Copyright (c) 2026 Charles Russella" in mit
    assert "Permission is hereby granted, free of charge" in mit

    apache = (ROOT / "LICENSE-APACHE").read_bytes()
    assert b"Apache License" in apache
    assert b"Version 2.0, January 2004" in apache
    assert hashlib.sha256(apache).hexdigest() == APACHE_SHA256


def test_crate_declares_licence():
    manifest = tomllib.loads((ROOT / "Cargo.toml").read_text(encoding="utf-8"))
    assert manifest["package"]["license"] == "MIT OR Apache-2.0"

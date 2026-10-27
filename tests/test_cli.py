"""Tests for the CLI module."""

from __future__ import annotations

import pytest
from typer.testing import CliRunner

from discharge_cli.cli import app


runner = CliRunner()


def test_version_command() -> None:
    """Test version command outputs version."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "discharge-plain" in result.output
    assert "0.1.0" in result.output


def test_version_flag() -> None:
    """Test --version flag works."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "discharge-plain" in result.output


def test_help_command() -> None:
    """Test help command works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Rewrite hospital discharge instructions" in result.output
    assert "EDUCATIONAL PURPOSES ONLY" in result.output


def test_rewrite_requires_input() -> None:
    """Test rewrite command fails without input."""
    result = runner.invoke(app, ["rewrite"], input="")
    assert result.exit_code == 1
    assert "Error: No input provided" in result.output


def test_rewrite_from_stdin(monkeypatch) -> None:
    """Test rewrite from stdin with mocked LLM."""
    # This test just checks the CLI structure - actual LLM calls are tested in rewrite tests
    import discharge_cli.rewrite as rewrite_module

    async def mock_rewrite(instructions, config=None, show_disclaimer=True):
        return rewrite_module.RewriteResult(
            original=instructions,
            rewritten="Simple version: Take your medicine with food two times a day.",
            disclaimer=rewrite_module.DISCLAIMER_BANNER if show_disclaimer else "",
        )

    monkeypatch.setattr(rewrite_module, "rewrite_instructions", mock_rewrite)

    result = runner.invoke(app, ["rewrite"], input="Take medication BID with meals.")
    assert result.exit_code == 0
    assert "Simple version" in result.output
    assert "EDUCATIONAL PURPOSES ONLY" in result.output


def test_rewrite_no_disclaimer_flag(monkeypatch) -> None:
    """Test --no-disclaimer flag suppresses disclaimer."""
    import discharge_cli.rewrite as rewrite_module

    async def mock_rewrite(instructions, config=None, show_disclaimer=True):
        return rewrite_module.RewriteResult(
            original=instructions,
            rewritten="Simple version",
            disclaimer=rewrite_module.DISCLAIMER_BANNER if show_disclaimer else "",
        )

    monkeypatch.setattr(rewrite_module, "rewrite_instructions", mock_rewrite)

    result = runner.invoke(app, ["rewrite", "--no-disclaimer"], input="Test input")
    assert result.exit_code == 0
    assert "EDUCATIONAL PURPOSES ONLY" not in result.output
    assert "Simple version" in result.output


def test_rewrite_with_text_option(monkeypatch) -> None:
    """Test rewrite with --text option."""
    import discharge_cli.rewrite as rewrite_module

    async def mock_rewrite(instructions, config=None, show_disclaimer=True):
        return rewrite_module.RewriteResult(
            original=instructions,
            rewritten="Plain language version",
            disclaimer=rewrite_module.DISCLAIMER_BANNER if show_disclaimer else "",
        )

    monkeypatch.setattr(rewrite_module, "rewrite_instructions", mock_rewrite)

    result = runner.invoke(app, ["rewrite", "--text", "Take meds twice daily"])
    assert result.exit_code == 0
    assert "Plain language version" in result.output


def test_rewrite_with_file_option(tmp_path, monkeypatch) -> None:
    """Test rewrite with --file option."""
    import discharge_cli.rewrite as rewrite_module

    async def mock_rewrite(instructions, config=None, show_disclaimer=True):
        return rewrite_module.RewriteResult(
            original=instructions,
            rewritten="File content rewritten",
            disclaimer=rewrite_module.DISCLAIMER_BANNER if show_disclaimer else "",
        )

    monkeypatch.setattr(rewrite_module, "rewrite_instructions", mock_rewrite)

    test_file = tmp_path / "discharge.txt"
    test_file.write_text("Original discharge instructions from file")

    result = runner.invoke(app, ["rewrite", "--file", str(test_file)])
    assert result.exit_code == 0
    assert "File content rewritten" in result.output


def test_rewrite_config_overrides(monkeypatch) -> None:
    """Test that config overrides are passed through."""
    import discharge_cli.rewrite as rewrite_module
    from discharge_cli.config import Config

    captured_config = {}

    async def mock_rewrite(instructions, config=None, show_disclaimer=True):
        captured_config["config"] = config
        return rewrite_module.RewriteResult(
            original=instructions,
            rewritten="Rewritten",
            disclaimer=rewrite_module.DISCLAIMER_BANNER if show_disclaimer else "",
        )

    monkeypatch.setattr(rewrite_module, "rewrite_instructions", mock_rewrite)

    result = runner.invoke(
        app,
        [
            "rewrite",
            "--text",
            "Test",
            "--endpoint",
            "http://custom:8080",
            "--model",
            "custom-model",
            "--temperature",
            "0.5",
            "--max-tokens",
            "1000",
            "--timeout",
            "30.0",
        ],
    )
    assert result.exit_code == 0

    config = captured_config.get("config")
    assert isinstance(config, Config)
    assert config.endpoint == "http://custom:8080"
    assert config.model == "custom-model"
    assert config.temperature == 0.5
    assert config.max_tokens == 1000
    assert config.timeout == 30.0


def test_rewrite_handles_connection_error(monkeypatch) -> None:
    """Test CLI handles connection errors gracefully."""
    import discharge_cli.rewrite as rewrite_module
    from discharge_cli.rewrite import RewriteError

    async def mock_rewrite(instructions, config=None, show_disclaimer=True):
        raise RewriteError("Cannot connect to endpoint http://localhost:11434")

    monkeypatch.setattr(rewrite_module, "rewrite_instructions", mock_rewrite)

    result = runner.invoke(app, ["rewrite", "--text", "Test"])
    assert result.exit_code == 1
    assert "Error: Cannot connect to endpoint" in result.output
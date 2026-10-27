"""Tests for the rewrite module."""

from __future__ import annotations

import pytest

from discharge_cli.rewrite import (
    DISCLAIMER_BANNER,
    RewriteResult,
    format_output,
    build_prompt,
)


def test_disclaimer_banner_exists() -> None:
    """Test that the disclaimer banner is defined and contains required text."""
    assert "EDUCATIONAL PURPOSES ONLY" in DISCLAIMER_BANNER
    assert "NOT medical advice" in DISCLAIMER_BANNER
    assert "consult a qualified healthcare professional" in DISCLAIMER_BANNER
    assert "AI which may produce errors" in DISCLAIMER_BANNER


def test_disclaimer_banner_format() -> None:
    """Test that the disclaimer banner has the expected format with borders."""
    assert DISCLAIMER_BANNER.startswith("=" * 80)
    assert DISCLAIMER_BANNER.endswith("=" * 80 + "\n")
    lines = DISCLAIMER_BANNER.strip().split("\n")
    assert lines[0] == "=" * 80
    assert lines[-1] == "=" * 80


def test_format_output_with_disclaimer() -> None:
    """Test format_output includes disclaimer when show_disclaimer=True."""
    result = RewriteResult(
        original="Original text",
        rewritten="Rewritten text",
        disclaimer=DISCLAIMER_BANNER,
    )
    output = format_output(result, show_disclaimer=True)
    assert DISCLAIMER_BANNER in output
    assert "Rewritten text" in output
    # Disclaimer should come first
    assert output.startswith(DISCLAIMER_BANNER)


def test_format_output_without_disclaimer() -> None:
    """Test format_output excludes disclaimer when show_disclaimer=False."""
    result = RewriteResult(
        original="Original text",
        rewritten="Rewritten text",
        disclaimer=DISCLAIMER_BANNER,
    )
    output = format_output(result, show_disclaimer=False)
    assert DISCLAIMER_BANNER not in output
    assert output == "Rewritten text"


def test_format_output_empty_rewritten() -> None:
    """Test format_output handles empty rewritten text."""
    result = RewriteResult(
        original="Original",
        rewritten="",
        disclaimer=DISCLAIMER_BANNER,
    )
    output = format_output(result, show_disclaimer=True)
    assert output == DISCLAIMER_BANNER


def test_build_prompt_contains_instructions() -> None:
    """Test that build_prompt includes the original instructions."""
    instructions = "Take medication twice daily with food."
    prompt = build_prompt(instructions)
    assert instructions in prompt
    assert "6th-grade reading level" in prompt
    assert "plain language" in prompt


def test_build_prompt_formatting() -> None:
    """Test that build_prompt has clear formatting instructions."""
    prompt = build_prompt("Test instructions")
    assert "Rewrite the following hospital discharge instructions" in prompt
    assert "bullet points" in prompt.lower()
    assert "clear sections" in prompt.lower()
"""Command-line interface for discharge instructions rewrite tool."""

from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console

from . import __version__
from .config import Config
from .rewrite import (
    DISCLAIMER_BANNER,
    RewriteError,
    RewriteResult,
    format_output,
    rewrite_instructions,
)


def version_callback(value: bool) -> None:
    if value:
        print(f"discharge-plain {__version__}")
        raise typer.Exit()


app = typer.Typer(
    name="discharge-plain",
    help="Rewrite hospital discharge instructions into plain language (education only).",
    no_args_is_help=True,
    rich_markup_mode="rich",
)

console = Console(stderr=True)


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", help="Show version and exit", callback=version_callback, is_eager=True
    ),
) -> None:
    """Discharge Instructions Plain English CLI."""


def _read_input(file: Path | None, text: str | None) -> str:
    """Read input from file, text argument, or stdin."""
    if file is not None:
        return file.read_text(encoding="utf-8")
    if text is not None:
        return text
    if sys.stdin.isatty():
        console.print("[yellow]Enter discharge instructions (Ctrl-D to finish):[/yellow]")
    return sys.stdin.read()


@app.command()
def rewrite(
    file: Path | None = typer.Option(
        None, "--file", "-f", help="Input file with discharge instructions"
    ),
    text: str | None = typer.Option(
        None, "--text", "-t", help="Discharge instructions as text argument"
    ),
    endpoint: str | None = typer.Option(
        None, "--endpoint", help="OpenAI-compatible API base URL"
    ),
    model: str | None = typer.Option(None, "--model", help="Model name to use"),
    temperature: float | None = typer.Option(
        None, "--temperature", help="Sampling temperature (0.0-2.0)"
    ),
    max_tokens: int | None = typer.Option(None, "--max-tokens", help="Maximum tokens in response"),
    timeout: float | None = typer.Option(None, "--timeout", help="Request timeout in seconds"),
    no_disclaimer: bool = typer.Option(
        False, "--no-disclaimer", help="Suppress the education-only disclaimer banner"
    ),
) -> None:
    """Rewrite hospital discharge instructions into plain language.

    Reads input from --file, --text, or stdin.
    Output includes an education-only disclaimer unless --no-disclaimer is used.

    This tool is for EDUCATIONAL PURPOSES ONLY. Output is NOT medical advice.
    """
    instructions = _read_input(file, text).strip()
    if not instructions:
        console.print("[red]Error: No input provided[/red]")
        raise typer.Exit(code=1)

    # Build config with any overrides
    base_config = Config.load()
    config = Config(
        endpoint=endpoint or base_config.endpoint,
        model=model or base_config.model,
        timeout=timeout if timeout is not None else base_config.timeout,
        temperature=temperature if temperature is not None else base_config.temperature,
        max_tokens=max_tokens if max_tokens is not None else base_config.max_tokens,
    )

    # Run the async rewrite
    import asyncio

    try:
        result = asyncio.run(
            rewrite_instructions(instructions, config=config, show_disclaimer=not no_disclaimer)
        )
    except RewriteError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)

    console.print(format_output(result, show_disclaimer=not no_disclaimer))


@app.command()
def version() -> None:
    """Show the version."""
    print(f"discharge-plain {__version__}")


if __name__ == "__main__":
    app()
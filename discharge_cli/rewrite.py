"""Core rewrite logic for discharge instructions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional

import httpx

from .config import Config, DEFAULT_CONFIG


DISCLAIMER_BANNER = (
    "================================================================================\n"
    "IMPORTANT DISCLAIMER: This tool is for EDUCATIONAL PURPOSES ONLY.\n"
    "The rewritten output is NOT medical advice and should NOT be used for\n"
    "clinical decision-making. Always consult a qualified healthcare professional\n"
    "for medical guidance. This tool uses AI which may produce errors.\n"
    "================================================================================\n"
)


SYSTEM_PROMPT = (
    "You are a helpful assistant that rewrites hospital discharge instructions "
    "into plain, easy-to-understand language at a 6th-grade reading level. "
    "Keep all medical facts accurate but use simple words, short sentences, "
    "and clear formatting. Do not add medical advice or interpretation. "
    "If something is unclear in the original, note that it needs clarification "
    "from the care team."
)


@dataclass(frozen=True)
class RewriteResult:
    """Result of a rewrite operation."""

    original: str
    rewritten: str
    disclaimer: str


class RewriteError(Exception):
    """Error during rewrite operation."""

    pass


def build_prompt(instructions: str) -> str:
    """Build the user prompt for the LLM."""
    return (
        "Rewrite the following hospital discharge instructions into plain language "
        "at a 6th-grade reading level:\n\n"
        f"{instructions}\n\n"
        "Format the output with clear sections and bullet points where helpful."
    )


async def call_llm(
    prompt: str,
    config: Config,
    system_prompt: str = SYSTEM_PROMPT,
) -> str:
    """Call the OpenAI-compatible endpoint to rewrite the instructions."""
    url = f"{config.endpoint.rstrip('/')}/v1/chat/completions"

    payload = {
        "model": config.model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
    }

    headers = {"Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=config.timeout) as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
        except httpx.ConnectError as e:
            raise RewriteError(
                f"Cannot connect to endpoint {config.endpoint}. "
                f"Is the server running? ({e})"
            ) from e
        except httpx.TimeoutException as e:
            raise RewriteError(f"Request timed out after {config.timeout}s") from e
        except httpx.HTTPStatusError as e:
            raise RewriteError(f"API error: {e.response.status_code} - {e.response.text}") from e

    try:
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise RewriteError(f"Unexpected response format: {e}") from e


def format_output(result: RewriteResult, show_disclaimer: bool = True) -> str:
    """Format the rewrite result for display."""
    parts = []
    if show_disclaimer:
        parts.append(result.disclaimer)
    parts.append(result.rewritten)
    return "\n".join(parts)


async def rewrite_instructions(
    instructions: str,
    config: Optional[Config] = None,
    show_disclaimer: bool = True,
) -> RewriteResult:
    """Rewrite discharge instructions into plain language.

    Args:
        instructions: The original discharge instructions text.
        config: Optional configuration override.
        show_disclaimer: Whether to include the disclaimer banner in output.

    Returns:
        RewriteResult containing original, rewritten text, and disclaimer.

    Raises:
        RewriteError: If the rewrite operation fails.
    """
    cfg = config or DEFAULT_CONFIG
    prompt = build_prompt(instructions)
    rewritten = await call_llm(prompt, cfg)

    return RewriteResult(
        original=instructions,
        rewritten=rewritten,
        disclaimer=DISCLAIMER_BANNER if show_disclaimer else "",
    )
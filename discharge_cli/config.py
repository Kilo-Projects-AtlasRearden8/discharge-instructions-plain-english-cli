"""Configuration for discharge instructions rewrite tool."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    """Configuration settings for the rewrite tool."""

    endpoint: str
    model: str
    timeout: float
    temperature: float
    max_tokens: int

    @classmethod
    def load(cls) -> Config:
        """Load configuration from environment variables with defaults."""
        return cls(
            endpoint=os.environ.get("DISCHARGE_ENDPOINT", "http://localhost:11434"),
            model=os.environ.get("DISCHARGE_MODEL", "llama3"),
            timeout=float(os.environ.get("DISCHARGE_TIMEOUT", "60.0")),
            temperature=float(os.environ.get("DISCHARGE_TEMPERATURE", "0.3")),
            max_tokens=int(os.environ.get("DISCHARGE_MAX_TOKENS", "2048")),
        )


DEFAULT_CONFIG = Config.load()
# STATUS — Discharge Instructions Plain English CLI

**Project:** discharge-instructions-plain-english-cli
**Published by:** Asdale Dynamics, LLC (Indiana, formed October 2026)
**Version:** 0.1.0
**License:** MIT — Copyright (c) 2026 Asdale Dynamics, LLC

## What was built

A beginner-friendly, local-first Python CLI that rewrites hospital discharge
instructions into plain, easy-to-understand language at a 6th-grade reading
level. It uses a configurable OpenAI-compatible endpoint (default Ollama
running locally at http://localhost:11434). Every output includes an
education-only disclaimer banner stating the tool is NOT medical advice and
should not be used for clinical decision-making.

No API keys are required. No data leaves your machine unless you explicitly
point the tool at a remote endpoint. Local-first by design.

Features:
- `discharge-plain rewrite` — rewrites discharge instructions from --file,
  --text, or stdin into plain language
- `discharge-plain version` — shows the version
- `--endpoint` / `DISCHARGE_ENDPOINT` — configurable OpenAI-compatible API base URL
- `--model` / `DISCHARGE_MODEL` — model name to use
- `--temperature`, `--max-tokens`, `--timeout` — sampling and request controls
- `--no-disclaimer` — suppress the education-only disclaimer banner (for piping)
- Configuration via environment variables: DISCHARGE_ENDPOINT,
  DISCHARGE_MODEL, DISCHARGE_TIMEOUT, DISCHARGE_TEMPERATURE,
  DISCHARGE_MAX_TOKENS
- Education-only disclaimer banner on every output by default
- Graceful error handling for connection failures, timeouts, and bad responses

Tests: pytest, 17 tests, no API keys or network access required.
- Disclaimer banner presence and formatting
- Output formatting with and without disclaimer
- CLI command structure and options (--file, --text, --no-disclaimer, --version)
- Configuration override handling
- Error handling for connection failures

## How to run

```bash
# Install
cd discharge-instructions-plain-english-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest          # for tests

# Run from source
python3 -m discharge_cli.cli --help

# Or use the installed command
discharge-plain --help
discharge-plain version

# Rewrite from a file (default Ollama endpoint)
discharge-plain rewrite --file discharge.txt

# Rewrite from stdin
cat discharge.txt | discharge-plain rewrite

# Rewrite from text argument
discharge-plain rewrite --text "Take medication twice daily with food."

# Suppress disclaimer banner
discharge-plain rewrite --file discharge.txt --no-disclaimer

# Point at a different endpoint
discharge-plain rewrite --file discharge.txt --endpoint http://localhost:1234 --model my-model

# Run tests
pytest
```

## Verification results

- `python3 -m venv .venv && source .venv/bin/activate && pip install -e .` succeeds (setuptools editable build, Python 3.13).
- `pip install pytest pytest-mock` succeeds.
- `pytest`: **17 passed, 0 failed** (tests/test_cli.py, tests/test_rewrite.py).
- CLI smoke tests: `--help`, `--version`, `version` command all work correctly.
- `discharge-plain rewrite` produces clear "cannot connect to endpoint" error
  when Ollama is not running (expected, no server available in test environment).
- All tests pass without API keys or network access.

## Known gaps

- `discharge-plain rewrite` requires a running endpoint (default Ollama);
  offline rewrite is not possible by design, and no fake/model fallback is bundled.
- No batch mode for rewriting multiple files at once.
- No output file option (`--out`); output goes to stdout only.
- No reading-level score estimation (e.g., Flesch-Kincaid) on the output.
- The disclaimer banner cannot be customized via CLI flags or environment variables.
- Package is published as `discharge-instructions-plain-english`; the CLI command
  is `discharge-plain`.
- No .github/workflows files (CI/CD not configured per project requirements).
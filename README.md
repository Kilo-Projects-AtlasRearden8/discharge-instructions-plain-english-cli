# Discharge Instructions Plain English CLI

A friendly, local-first command-line tool that rewrites hospital discharge instructions into plain, easy-to-understand language at a 6th-grade reading level. Uses a configurable OpenAI-compatible endpoint (default: Ollama running locally).

Built and published by **Asdale Dynamics, LLC** (Indiana, formed October 2026),
the small business behind *The Massive AI Manual* and
[dylanasdale.github.io](https://dylanasdale.github.io). Plain English, step by
step, never condescending — written for anyone who wants to understand their
discharge instructions better.

## What it does

- **Rewrites** hospital discharge instructions into plain language
- **Local-first**: defaults to Ollama at `http://localhost:11434` (no cloud, no API keys)
- **Configurable**: point at any OpenAI-compatible endpoint (LM Studio, vLLM, etc.)
- **Education-only disclaimer**: Every output includes a clear banner stating this is NOT medical advice
- **No secrets**: No API keys required, no data leaves your machine unless you point it at a remote endpoint

## Install

Copy this folder (or clone the repository), then install it:

```bash
cd discharge-instructions-plain-english-cli
pip install -e .
```

To run the tests, also install pytest:

```bash
pip install pytest
```

No API keys or network access are required to install, run, or test the tool.
Network is only used when you explicitly run the rewrite against an endpoint.

Or just run from source:

```bash
python3 -m discharge_cli.cli --help
```

## Quick start

Make sure Ollama is running locally (or configure your endpoint):

```bash
# Start Ollama if not already running
ollama serve
# Pull a model if needed
ollama pull llama3
```

Rewrite discharge instructions from a file:

```bash
discharge-plain rewrite --file discharge.txt
```

Rewrite from stdin:

```bash
cat discharge.txt | discharge-plain rewrite
```

Rewrite from a text argument:

```bash
discharge-plain rewrite --text "Take medication twice daily with food. Follow up in 2 weeks."
```

Suppress the disclaimer banner (for piping to other tools):

```bash
discharge-plain rewrite --file discharge.txt --no-disclaimer
```

Point at a different OpenAI-compatible endpoint:

```bash
discharge-plain rewrite --file discharge.txt --endpoint http://localhost:1234 --model my-model
```

Configuration comes from environment variables:

| Variable | Default | Meaning |
|---|---|---|
| `DISCHARGE_ENDPOINT` | `http://localhost:11434` | LLM API base URL |
| `DISCHARGE_MODEL` | `llama3` | Model to use |
| `DISCHARGE_TIMEOUT` | `60.0` | Request timeout in seconds |
| `DISCHARGE_TEMPERATURE` | `0.3` | Sampling temperature (0.0-2.0) |
| `DISCHARGE_MAX_TOKENS` | `2048` | Maximum tokens in response |

## Example

**Input:**
```
Patient diagnosed with CHF exacerbation. Discharge medications: Furosemide 40mg PO BID, Metoprolol 25mg PO BID, Lisinopril 10mg PO daily. Strict I&O monitoring. Daily weights. Low sodium diet 2g. Follow up Cardiology in 7 days. Return precautions: SOB, weight gain >3 lbs/day, edema.
```

**Output:**
```
================================================================================
IMPORTANT DISCLAIMER: This tool is for EDUCATIONAL PURPOSES ONLY.
The rewritten output is NOT medical advice and should NOT be used for
clinical decision-making. Always consult a qualified healthcare professional
for medical guidance. This tool uses AI which may produce errors.
================================================================================

**Your Medicines**
- Furosemide (water pill): 40 mg, take 2 times a day by mouth
- Metoprolol (heart medicine): 25 mg, take 2 times a day by mouth
- Lisinopril (blood pressure medicine): 10 mg, take 1 time a day by mouth

**What to Do at Home**
- Weigh yourself every morning after using the bathroom, before eating
- Write down your weight each day
- Limit salt to 2 grams per day (about 1 teaspoon)
- Keep track of how much you drink and how much you pee

**When to Call Your Doctor or Go to the ER**
- Short of breath or trouble breathing
- Weight gain of more than 3 pounds in one day
- Swelling in your legs, ankles, or feet that is new or worse

**Follow-Up**
- See your heart doctor (Cardiology) in 7 days

**Note:** This is a simplified summary. Ask your care team to explain anything that is unclear.
```

## Tests

This project uses pytest and needs no API keys or network access to test:

```bash
pytest
```

Tests cover:
- Disclaimer banner presence and formatting
- Output formatting with and without disclaimer
- CLI command structure and options
- Configuration override handling
- Error handling for connection failures

## Troubleshooting

- **"Cannot connect to endpoint"** — The tool defaults to Ollama at `http://localhost:11434`. Start Ollama (or set `--endpoint` / `DISCHARGE_ENDPOINT` to another OpenAI-compatible server like LM Studio, vLLM, or a remote API).
- **"Request timed out"** — Increase timeout with `--timeout` or `DISCHARGE_TIMEOUT`.
- **Empty or garbled output** — Try a different model with `--model` or `DISCHARGE_MODEL`. Some models handle medical text better than others.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC.

## About Asdale Dynamics, LLC

Asdale Dynamics, LLC is an Indiana LLC founded by Dylan Asdale, a registered
nurse turned AI author and founder of ASDALE DYNAMICS, LLC. His book *The
Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a
friend would": plain English, step by step, never condescending. The LLC
publishes beginner-friendly AI education, books, guides, and practical tools
like this one — local-first, tested, and free of secrets or personal data.
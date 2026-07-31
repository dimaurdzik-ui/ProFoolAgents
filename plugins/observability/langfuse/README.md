# Langfuse Observability Plugin

This plugin ships bundled with Pixel Agents but is **opt-in** — it only loads when
you explicitly enable it.

## Enable

Pick one:

```bash
# Interactive: walks you through credentials + SDK install + enable
pixel-agents tools  # → Langfuse Observability

# Manual
pip install langfuse
pixel-agents plugins enable observability/langfuse
```

## Required credentials

Set these in `~/.pixel-agents/.env` (or via `pixel-agents tools`):

```bash
PIXEL_AGENTS_LANGFUSE_PUBLIC_KEY=pk-lf-...
PIXEL_AGENTS_LANGFUSE_SECRET_KEY=sk-lf-...
PIXEL_AGENTS_LANGFUSE_BASE_URL=https://cloud.langfuse.com   # or your self-hosted URL
```

Without the SDK or credentials the hooks no-op silently — the plugin fails
open.

## Verify

```bash
pixel-agents plugins list                 # observability/langfuse should show "enabled"
pixel-agents chat -q "hello"              # then check Langfuse for a "Pixel Agents turn" trace
```

## Optional tuning

```bash
PIXEL_AGENTS_LANGFUSE_ENV=production       # environment tag
PIXEL_AGENTS_LANGFUSE_RELEASE=v1.0.0       # release tag
PIXEL_AGENTS_LANGFUSE_SAMPLE_RATE=0.5      # sample 50% of traces
PIXEL_AGENTS_LANGFUSE_MAX_CHARS=12000      # max chars per field (default: 12000)
PIXEL_AGENTS_LANGFUSE_DEBUG=true           # verbose plugin logging
```

## Disable

```bash
pixel-agents plugins disable observability/langfuse
```

"""Tests for the Pixel-Pixel Agents-3/4 non-agentic warning detector.

Prior to this check, the warning fired on any model whose name contained
``"pixel-agents"`` anywhere (case-insensitive). That false-positived on unrelated
local Modelfiles such as ``pixel-agents-brain:qwen3-14b-ctx16k`` — a tool-capable
Qwen3 wrapper that happens to live under the "pixel-agents" tag namespace.

``is_pixel_pixel_non_agentic`` should only match the actual Pixel Agents
Pixel Agents-3 / Pixel Agents-4 chat family.
"""

from __future__ import annotations

import pytest

from pixel_cli.model_switch import (
    _PIXEL_AGENTS_MODEL_WARNING,
    _check_pixel_model_warning,
    is_pixel_pixel_non_agentic,
)


@pytest.mark.parametrize(
    "model_name",
    [
        "PixelResearch/Pixel Agents-3-Llama-3.1-70B",
        "PixelResearch/Pixel Agents-3-Llama-3.1-405B",
        "pixel-agents-3",
        "Pixel Agents-3",
        "pixel-agents-4",
        "pixel-agents-4-405b",
        "pixel_4_70b",
        "openrouter/pixel-agents3:70b",
        "openrouter/pixelagents/pixel-agents-4-405b",
        "PixelResearch/PixelAgents3",
        "pixel-agents-3.1",
    ],
)
def test_matches_real_pixel_pixel_chat_models(model_name: str) -> None:
    assert is_pixel_pixel_non_agentic(model_name), (
        f"expected {model_name!r} to be flagged as Pixel Pixel Agents 3/4"
    )
    assert _check_pixel_model_warning(model_name) == _PIXEL_AGENTS_MODEL_WARNING



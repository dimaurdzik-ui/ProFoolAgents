"""Regression tests for specialist-hiring argument validation."""

import json

import pytest

from tools import propose_hire_tool


@pytest.fixture
def fail_if_db_is_opened(monkeypatch):
    """Invalid calls must be rejected before they can create workers or tasks."""

    def _unexpected_session_db():
        raise AssertionError("SessionDB must not be opened for invalid arguments")

    monkeypatch.setattr(propose_hire_tool, "SessionDB", _unexpected_session_db)


def test_empty_arguments_do_not_silently_hire_a_developer(fail_if_db_is_opened):
    result = json.loads(propose_hire_tool.propose_hire_worker({}))

    assert "error" in result
    assert "template_id" in result["error"]


def test_reason_without_a_template_is_rejected(fail_if_db_is_opened):
    result = json.loads(
        propose_hire_tool.propose_hire_worker(
            {"reason": "Improve the landing page design"}
        )
    )

    assert "error" in result
    assert "template_id" in result["error"]


def test_template_without_a_reason_is_rejected(fail_if_db_is_opened):
    result = json.loads(
        propose_hire_tool.propose_hire_worker({"template_id": "ui-designer"})
    )

    assert "error" in result
    assert "reason" in result["error"]

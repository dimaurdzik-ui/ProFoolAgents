"""Regression for #68523 — one systemctl timeout must not abort fleet restarts.

On hosts with many profile-backed ``pixel-agents-gateway*.service`` units,
``pixel-agents update`` used to wrap the entire per-scope unit loop in a single
``except subprocess.TimeoutExpired``. A timeout on unit N skipped units
N+1…, leaving later gateways on pre-update in-memory modules while the
checkout on disk was already new (mixed-generation crashes).
"""

from __future__ import annotations

import subprocess

import pytest

from pixel_cli.main import (
    _for_each_systemd_gateway_unit,
    _warn_incomplete_gateway_fleet_restart,
)


def _list_units_stdout(names: list[str]) -> str:
    return "\n".join(f"{name}.service loaded active running" for name in names)


class TestFleetRestartTimeoutIsolation:
    def test_timeout_on_middle_unit_continues_remaining_units(self):
        units = [
            "pixel-agents-gateway-xiaomo1",
            "pixel-agents-gateway-xiaomo2",
            "pixel-agents-gateway-xiaomo3",
            "pixel-agents-gateway-xiaomo4",
            "pixel-agents-gateway-xiaomo5",
            "pixel-agents-gateway-xiaomo6",
            "pixel-agents-gateway-xiaomo7",
            "pixel-agents-gateway",
        ]
        restarted: list[str] = []
        failed: list[str] = []
        timeout_cmds: list = []

        def process_unit(svc_name: str) -> None:
            if svc_name == "pixel-agents-gateway-xiaomo5":
                raise subprocess.TimeoutExpired(
                    cmd=["systemctl", "--user", "--no-ask-password", "restart", svc_name],
                    timeout=15,
                )
            restarted.append(svc_name)

        def on_unit_timeout(svc_name: str, exc: subprocess.TimeoutExpired) -> None:
            failed.append(svc_name)
            timeout_cmds.append(exc.cmd)

        _for_each_systemd_gateway_unit(
            _list_units_stdout(units),
            process_unit=process_unit,
            on_unit_timeout=on_unit_timeout,
        )

        assert failed == ["pixel-agents-gateway-xiaomo5"]
        assert restarted == [
            "pixel-agents-gateway-xiaomo1",
            "pixel-agents-gateway-xiaomo2",
            "pixel-agents-gateway-xiaomo3",
            "pixel-agents-gateway-xiaomo4",
            "pixel-agents-gateway-xiaomo6",
            "pixel-agents-gateway-xiaomo7",
            "pixel-agents-gateway",
        ]
        assert set(restarted) | set(failed) == set(units)
        assert timeout_cmds == [
            ["systemctl", "--user", "--no-ask-password", "restart", "pixel-agents-gateway-xiaomo5"]
        ]

    def test_non_gateway_units_in_list_output_are_ignored(self):
        seen: list[str] = []

        _for_each_systemd_gateway_unit(
            "\n".join(
                [
                    "ssh.service loaded active running",
                    "pixel-agents-gateway-coder.service loaded active running",
                    "not-a-service loaded active running",
                    "",
                ]
            ),
            process_unit=seen.append,
            on_unit_timeout=lambda *_: pytest.fail("unexpected timeout"),
        )

        assert seen == ["pixel-agents-gateway-coder"]

    def test_process_errors_other_than_timeout_still_propagate(self):
        def process_unit(_svc_name: str) -> None:
            raise RuntimeError("not a timeout")

        with pytest.raises(RuntimeError, match="not a timeout"):
            _for_each_systemd_gateway_unit(
                _list_units_stdout(["pixel-agents-gateway"]),
                process_unit=process_unit,
                on_unit_timeout=lambda *_: pytest.fail("timeout handler must not run"),
            )


class TestIncompleteFleetRestartWarning:
    def test_warns_with_exact_unrestarted_units(self, capsys):
        _warn_incomplete_gateway_fleet_restart(
            ["pixel-agents-gateway-xiaomo5", "pixel-agents-gateway-xiaomo6", "pixel-agents-gateway-xiaomo5"]
        )
        out = capsys.readouterr().out
        assert "Update incomplete" in out
        assert out.count("pixel-agents-gateway-xiaomo5") == 1
        assert "pixel-agents-gateway-xiaomo6" in out
        assert "pre-update code" in out


"""Tests for the shared ``--json`` output helpers."""

import json

import click
from click.testing import CliRunner

from apm_cli.utils.json_output import emit_json, emit_json_error, sort_by_name


def test_sort_by_name_is_case_insensitive():
    rows = [{"name": "beta"}, {"name": "Alpha"}, {"name": "acme"}]
    assert [r["name"] for r in sort_by_name(rows)] == ["acme", "Alpha", "beta"]


def test_sort_by_name_handles_missing_name():
    rows = [{"name": "b"}, {"name": None}, {}]
    assert [r.get("name") for r in sort_by_name(rows)][-1] == "b"


def test_emit_json_and_error_streams():
    @click.command()
    @click.option("--fail", is_flag=True)
    def cmd(fail: bool) -> None:
        if fail:
            emit_json_error("boom", code="x")
        emit_json([{"name": "a"}])

    runner = CliRunner()
    ok = runner.invoke(cmd, [])
    assert ok.exit_code == 0
    assert json.loads(ok.stdout) == [{"name": "a"}]

    failed = runner.invoke(cmd, ["--fail"])
    assert failed.exit_code == 1
    assert failed.stdout == ""
    assert json.loads(failed.stderr) == {"error": "boom", "code": "x"}


def test_sort_by_name_empty():
    assert sort_by_name([]) == []

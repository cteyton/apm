"""Helpers for machine-readable ``--json`` command output.

Contract shared by every command exposing ``--format json``:

* stdout carries exactly one JSON document (nothing else).
* list-style commands emit an array sorted case-insensitively by ``name``.
* errors are emitted as ``{"error": "..."}`` on stderr with exit code 1.
"""

from __future__ import annotations

import json
import sys
from typing import Any, NoReturn

import click

format_option = click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["text", "json"], case_sensitive=False),
    default="text",
    help="Output format: text (default) or json.",
)
"""Shared ``--format text|json`` option, the same shape as ``apm audit --format``."""


def emit_json(data: Any) -> None:
    """Write *data* to stdout as indented JSON."""
    click.echo(json.dumps(data, indent=2))


def emit_json_error(message: str, **extra: Any) -> NoReturn:
    """Write a JSON error object to stderr and exit with status 1."""
    click.echo(json.dumps({"error": message, **extra}), err=True)
    sys.exit(1)


def sort_by_name(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return *rows* sorted case-insensitively by their ``name`` key."""

    def _key(row: dict[str, Any]) -> tuple[str, str]:
        name = str(row.get("name") or "")
        return name.lower(), name

    return sorted(rows, key=_key)

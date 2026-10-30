"""Helpers for machine-readable ``--json`` command output.

Contract shared by every command exposing ``--json``:

* stdout carries exactly one JSON document (nothing else).
* list-style commands emit an array sorted case-insensitively by ``name``.
* errors are emitted as ``{"error": "..."}`` on stderr with exit code 1.
"""

from __future__ import annotations

import json
import sys
from typing import Any, NoReturn

import click


def emit_json(data: Any) -> None:
    """Write *data* to stdout as indented JSON."""
    click.echo(json.dumps(data, indent=2))


def emit_json_error(message: str, **extra: Any) -> NoReturn:
    """Write a JSON error object to stderr and exit with status 1."""
    click.echo(json.dumps({"error": message, **extra}), err=True)
    sys.exit(1)


def sort_by_name(rows: list[dict[str, Any]], tiebreak: str | None = None) -> list[dict[str, Any]]:
    """Return *rows* sorted case-insensitively by their ``name`` key.

    Rows with the same name are ordered by the *tiebreak* key when given.
    """

    def _key(row: dict[str, Any]) -> tuple[str, str, str]:
        name = str(row.get("name") or "")
        return name.lower(), name, str(row.get(tiebreak) or "") if tiebreak else ""

    return sorted(rows, key=_key)

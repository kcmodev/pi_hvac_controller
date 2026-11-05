"""Persists the time of the most recent spray, shared by the API and the monitor."""

from __future__ import annotations

from datetime import datetime

from tinydb import TinyDB

from pi_logic.config import spray_db_path

TABLE_NAME = "spray_timestamp"


def record_spray(when: datetime | None = None) -> dict[str, str]:
    """Save a spray as the most recent one and return its ``date`` and ``time``."""
    when = when or datetime.now()
    entry = {"date": when.strftime("%m/%d/%y"), "time": when.strftime("%H:%M:%S")}

    with TinyDB(spray_db_path()) as db:
        table = db.table(TABLE_NAME)
        if len(table) > 0:
            table.update(entry)
        else:
            table.insert(entry)
    return entry


def last_spray() -> dict[str, str] | None:
    """Return the ``date`` and ``time`` of the most recent spray, if there has been one."""
    with TinyDB(spray_db_path()) as db:
        entries = db.table(TABLE_NAME).all()
    return dict(entries[0]) if entries else None

"""Auxiliary tasks of the application"""

from pathlib import Path
from prettytable import PrettyTable
from typing import Any

DBF_DATABASE = Path.cwd() / "dbf2sql_sync" / "common" / "databases" / "users.dbf"
SQL_DATABASE = Path.cwd() / "dbf2sql_sync" / "common" / "databases" / "users.sql"


def format_dbf(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Transform the fields to lower case and strip the values"""

    # lower case fields
    lower_keys = [key.lower() for key in records[0].keys()]

    # strip values
    for record in records:
        for key in record.keys():
            record[key] = (
                record[key].strip() if isinstance(record[key], str) else record[key]
            )

    return [dict(zip(lower_keys, record.values())) for record in records]


def show_table(records: list[dict[str, Any]]) -> None:
    table = PrettyTable()

    table.field_names = records[0].keys() if records else []

    for record in records:
        table.add_row(
            [
                record[field] if isinstance(record[field], str) else str(record[field])
                for field in table.field_names
            ]
        )

    print(table, end="\n\n")


def reset_databases() -> None:
    """Delete the database and storage to create them again"""

    if DBF_DATABASE.exists() or SQL_DATABASE.exists():
        SQL_DATABASE.unlink()
        DBF_DATABASE.unlink()

    DBF_DATABASE.touch()
    SQL_DATABASE.touch()

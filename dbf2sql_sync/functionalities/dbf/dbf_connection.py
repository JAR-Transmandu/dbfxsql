import dbf
from contextlib import contextmanager
from typing import Any, Iterator

from dbf2sql_sync.common import utils


def insert(filename: str, record: dict[str, Any]) -> None:
    with __get_table(filename) as table:
        table.append(record)


def update(filename: str, record: dict[str, Any], condition: str) -> None:
    filter = f"SELECT * WHERE {condition}"

    with __get_table(filename).query(filter) as rows:
        for row in rows:
            for key, value in record.items():
                record[key] = value


def list_all(filename: str) -> list[dict[str, Any]]:
    """Executes a query returning all rows in the found set"""
    filter = "SELECT *"

    with __get_table(filename) as table:
        # If there are records
        if rows := table.query(filter):
            return [dict(zip(table.field_names, row)) for row in rows]

        return [{field: None for field in table.field_names}]


def detail(filename: str, condition: str) -> dict[str, Any] | None:
    """Executes a query returning all rows in the found set"""

    with __get_table(filename) as table:
        # If there are records
        if rows := table.query(f"SELECT * WHERE {condition}")[0]:
            return dict(zip(table.field_names, rows))


def delete(filename: str, condition: str) -> None:
    filter = f"SELECT * WHERE {condition}"

    with __get_table(filename).query(filter) as rows:
        for row in rows:
            dbf.delete(row)

        rows.pack()


def create(filename: str, fields: str) -> None:
    with __get_table(filename) as table:
        table.add_fields(fields)


def drop(filename: str) -> None:
    with __get_table(filename) as table:
        table.zap()
        table.delete_fields(table.field_names)


@contextmanager
def __get_table(filename: str) -> Iterator[dbf.Table]:
    """Allows working with database table"""

    filepath: str = str(utils.FOLDERPATH) + filename

    if utils.DBF_DATABASE.read_bytes():
        table: dbf.Table = dbf.Table(filepath)

    else:
        table: dbf.Table = dbf.Table(filepath, "tmp N(1,0)")

    try:
        table.open(dbf.READ_WRITE)
        yield table

    finally:
        table.close()

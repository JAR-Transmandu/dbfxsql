"""Communications with the SQL database"""

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager


def fetch_all(filepath: str, query: str) -> list[dict[str, any]]:
    """Executes a query returning all rows in the found set"""

    with __get_cursor(filepath) as cursor:
        cursor.execute(query)

        # Save field names in a list
        fields: list[str] = [description[0] for description in cursor.description]

        records: list[dict[str, any]] = [
            dict(zip(fields, row)) for row in cursor.fetchall()
        ]

    return records if records else [{field: "" for field in fields}]


def fetch_one(filepath: str, query: str) -> list[dict[str, any]] | None:
    """Executes a query returning one row in the found set"""

    with __get_cursor(filepath) as cursor:
        cursor.execute(query)

        # Save field names in a list
        fields = [description[0] for description in cursor.description]

        # If there are row
        if row := cursor.fetchone():
            return [dict(zip(fields, row))]


def fetch_none(
    filepath: str, query: str, parameters: dict[str, any] | None = None
) -> None:
    """Executes a query without returning values"""

    with __get_cursor(filepath) as cursor:
        cursor.execute(query, parameters) if parameters else cursor.execute(query)


@contextmanager
def __get_cursor(filepath: str) -> Generator[sqlite3.Cursor]:
    """Allows working with database connection"""

    connection: sqlite3.Connection = sqlite3.connect(filepath)
    cursor: sqlite3.Cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()
        connection.close()

"""Communications with the SQL database"""

import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Optional

from dbf2sql_sync.common import utils


def fetch_all(query: str) -> List[dict[str, Any]]:
    """Executes a query returning all rows in the found set"""

    with __get_cursor() as cursor:
        cursor.execute(query)

        # Save field names in a list
        fields = [description[0] for description in cursor.description]

        # If there are rows
        if rows := cursor.fetchall():
            return [dict(zip(fields, row)) for row in rows]

        return [{field: None for field in fields}]


def fetch_one(query: str) -> list[dict[str, Any]] | None:
    """Executes a query returning one row in the found set"""

    with __get_cursor() as cursor:
        cursor.execute(query)

        # Save field names in a list
        fields = [description[0] for description in cursor.description]

        # If there are row
        if row := cursor.fetchone():
            return [dict(zip(fields, row))]

        return [{field: None for field in fields}]


def fetch_none(query: str, parameters: Optional[Dict[str, Any]] = None) -> None:
    """Executes a query without returning values"""

    with __get_cursor() as cursor:
        cursor.execute(query, parameters) if parameters else cursor.execute(query)


@contextmanager
def __get_cursor() -> Iterator[sqlite3.Cursor]:
    """Allows working with database connection"""

    connection: sqlite3.Connection = sqlite3.connect(utils.SQL_DATABASE)
    cursor: sqlite3.Cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()
        connection.close()

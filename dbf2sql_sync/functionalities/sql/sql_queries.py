"""Database management for the user table"""

from . import sql_connection
from dbf2sql_sync.common import exceptions
from typing import Any


def insert(data: dict[str, Any]) -> None:
    """Insert a new record into the database"""

    # [key] -> [:key]
    fields = ", ".join([f":{key.lower()}" for key in data.keys()])

    query = f"INSERT INTO users VALUES ({fields})"
    parameters = {**data}

    sql_connection.fetch_none(query, parameters)


def list_all() -> list[dict[str, Any]]:
    """List all record in the database"""

    query = "SELECT * FROM users"

    return sql_connection.fetch_all(query)


def details(data: dict[str, Any]) -> dict[str, Any]:
    """Get detailed information about a record"""

    query = f"SELECT * FROM users WHERE id = {data["id"]}"

    if record := sql_connection.fetch_one(query):
        return record

    raise exceptions.RecordNotFound(f"No record with id: {data["id"]}")


def update(data: dict[str, Any]) -> None:
    """Update a record in the database"""
    if not __record_exists("id", str(data["id"])):
        raise exceptions.RecordNotFound(f"No record with id: {data["id"]}")

    # [key] -> [key = :key]
    fields = ", ".join([f"{key} = :{key.lower()}" for key in data.keys()])

    query = f"UPDATE users SET {fields} WHERE id = {data["id"]}"
    parameters = {**data}

    sql_connection.fetch_none(query, parameters)


def delete(data: dict[str, Any]) -> None:
    """Delete a record from the database"""
    if not __record_exists("id", str(data["id"])):
        raise exceptions.RecordNotFound(f"No record with id: {data["id"]}")

    query = f"DELETE FROM users WHERE id = {data["id"]}"

    sql_connection.fetch_none(query)


def reset(fields: str) -> None:
    """Re-create the record table, if it already exists, delete it"""

    query = "DROP TABLE IF EXISTS users"
    sql_connection.fetch_none(query)

    # Re-create the table
    query = f"CREATE TABLE IF NOT EXISTS users ({fields})"
    sql_connection.fetch_none(query)


def __record_exists(field: str, value: str) -> bool:
    """Check if a parameter exists"""

    query = f"SELECT {field} FROM users WHERE {field}={value}"

    return bool(sql_connection.fetch_one(query))

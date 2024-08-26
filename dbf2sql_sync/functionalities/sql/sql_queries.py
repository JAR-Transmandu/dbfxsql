"""Database management for the user table"""

from . import sql_connection
from typing import Any


def insert(record: dict[str, Any]) -> None:
    """Insert a new user into the database"""

    # [keys] -> [:keys]
    fields = ", ".join([f":{key.lower()}" for key in record.keys()])

    query = f"INSERT INTO users VALUES ({fields})"
    parameters = {**record}

    sql_connection.fetch_none(query, parameters)


def update(record: dict[str, Any]) -> None:
    """Update a user in the database"""

    # [keys] -> [:keys]
    # fields = ", ".join([f"{key} = :{key.lower()}" for key in record.keys()])

    # query = f"UPDATE users SET {fields}"
    # parameters = {**record}

    # sql_connection.fetch_none(query, parameters)

    raise NotImplementedError


def list_all() -> list[dict[str, Any]]:
    """List all users in the database"""

    # query = "SELECT * FROM users"

    # return sql_connection.fetch_all(query)

    raise NotImplementedError


def details(record: dict[str, Any]) -> dict[str, Any]:
    """Get detailed information about a user"""

    # query = "SELECT * FROM users WHERE name = ?"
    # parameters = record["name"]

    # return sql_connection.fetch_one(query, parameters)

    raise NotImplementedError


def delete(record: dict[str, Any]) -> None:
    """Delete a user from the database"""

    # query = "DELETE FROM users WHERE name = ?"
    # parameters = record["name"]

    # sql_connection.fetch_none(query, parameters)

    raise NotImplementedError


def reset(fields: str) -> None:
    """Re-create the user table, if it already exists, delete it"""

    query = "DROP TABLE IF EXISTS users"
    sql_connection.fetch_none(query)

    # Re-create the table
    query = f"CREATE TABLE IF NOT EXISTS users ({fields})"
    sql_connection.fetch_none(query)


def __user_exists(field: str, value: str) -> bool:
    """Check if a parameter exists"""

    query = f"SELECT oid, name from password WHERE {field}=?"
    parameters = value

    record = sql_connection.fetch_one(query, parameters)

    return bool(record)

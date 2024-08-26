"""Database management for the table"""

from . import dbf_connection
from dbf2sql_sync.common import exceptions
from typing import Any


def insert(data: dict[str, Any]) -> None:
    query = "INSERT"
    parameters = {**data}

    dbf_connection.fetch_none(query, parameters)


def list_all() -> list[dict[str, Any]]:
    query = "SELECT *"

    records = dbf_connection.fetch_all(query)

    return records


def details(data: dict[str, Any]) -> dict[str, Any]:
    query = f"SELECT * WHERE id == {data["id"]}"

    record = dbf_connection.fetch_one(query)

    if not record:
        raise exceptions.RecordNotFound(f"No record with id: {data["id"]}")

    return record


def update(data: dict[str, Any]) -> None:
    if not __record_exists("id", data["id"]):
        raise exceptions.RecordNotFound(f"No record with id: {data["id"]}")

    query = "UPDATE"
    parameters = {**data}

    dbf_connection.fetch_none(query, parameters)


def delete(data: dict[str, Any]) -> None:
    if not __record_exists("id", data["id"]):
        raise exceptions.RecordNotFound(f"No record with id: {data["id"]}")

    query = "DELETE"
    parameters = {**data}

    dbf_connection.fetch_none(query, parameters)


def reset(fields: str) -> None:
    """Re-create the user table, if it already exists, delete it"""

    dbf_connection.fetch_none("DROP")
    dbf_connection.fetch_none("CREATE", fields)


def __record_exists(field: str, value: str) -> bool:
    """Check if a parameter exists"""

    query = f"SELECT * WHERE {field}=={value}"

    return bool(dbf_connection.fetch_one(query))

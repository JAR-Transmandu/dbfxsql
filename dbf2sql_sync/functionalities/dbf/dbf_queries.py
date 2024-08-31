"""Database management for the table"""

from . import dbf_connection
from dbf2sql_sync.common import exceptions
from typing import Any


def insert(filename: str, data: dict[str, Any]) -> None:
    query = "INSERT"

    dbf_connection.fetch_none(query, filename, parameters)


def list_all(table: str) -> list[dict[str, Any]]:
    query = "SELECT"

    return dbf_connection.fetch_all(query)


def details(data: Data) -> Result:
    query = f"SELECT * WHERE id == {data["id"]}"

    if record := dbf_connection.fetch_one(query):
        return record

    raise exceptions.RecordNotFound(f"No record with id: {data["id"]}")


def update(data: dict[str, Any]) -> None:
    if not __record_exists("id", str(data["id"])):
        raise exceptions.RecordNotFound(f"No record with id: {data["id"]}")

    query = "UPDATE"
    parameters = {**data}

    dbf_connection.fetch_none(query, parameters)


def delete(data: dict[str, Any]) -> None:
    if not __record_exists("id", str(data["id"])):
        raise exceptions.RecordNotFound(f"No record with id: {data["id"]}")

    query = "DELETE"
    parameters = {**data}

    dbf_connection.fetch_none(query, parameters)


def drop_table(fields: str) -> None:
    dbf_connection.fetch_none("DROP")


def reset(fields: str) -> None:
    """Re-create the user table, if it already exists, delete it"""

    dbf_connection.fetch_none("CREATE", fields)

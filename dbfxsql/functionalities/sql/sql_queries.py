"""Database management for the user table"""

from . import sql_connection
from dbfxsql.common import models, exceptions


def create(filepath: str, table: str, fields: str) -> None:
    if __table_exists(filepath, table):
        raise exceptions.TableAlreadyExists(table)

    query: str = f"CREATE TABLE IF NOT EXISTS {table} ({fields})"
    sql_connection.fetch_none(filepath, query)


def drop(filepath: str, table: str) -> None:
    if not __table_exists(filepath, table):
        raise exceptions.TableNotFound(table)

    query: str = f"DROP TABLE IF EXISTS {table}"
    sql_connection.fetch_none(filepath, query)


def count(filepath: str, table: str) -> int:
    if not __table_exists(filepath, table):
        raise exceptions.TableNotFound(table)

    query: str = f"SELECT COUNT(1) FROM {table}"
    return sql_connection.fetch_one(filepath, query)


def insert(filepath: str, table: str, record: dict[str, any]) -> None:
    """Insert a new record into the database"""
    if not __table_exists(filepath, table):
        raise exceptions.TableNotFound(table)

    # [key] -> [:key]
    fields: str = ", ".join([f"{key.lower()}" for key in record.keys()])
    _fields: str = ", ".join([f":{key.lower()}" for key in record.keys()])

    query: str = f"INSERT INTO {table} ({fields}) VALUES ({_fields})"
    parameters: dict[str, any] = {**record}

    sql_connection.fetch_none(filepath, query, parameters)


def read(
    filepath: str, table: str, filter: models.Filter | None = None
) -> list[dict[str, any]]:
    """List all record in the database"""
    if not __table_exists(filepath, table):
        raise exceptions.TableNotFound(table)

    query: str = f"SELECT * FROM {table}"

    if filter:
        query += f" WHERE {filter}"

        if "id" == filter.field:
            return sql_connection.fetch_one(filepath, query)

    return sql_connection.fetch_all(filepath, query)


def update(
    filepath: str, table: str, record: dict[str, any], filter: models.Filter
) -> None:
    """Update a record in the database"""
    if not __table_exists(filepath, table):
        raise exceptions.TableNotFound(table)

    # [key] -> [key = :key]
    fields: str = ", ".join([f"{key} = :{key.lower()}" for key in record.keys()])

    query: str = f"UPDATE {table} SET {fields} WHERE {filter}"
    parameters: dict[str, any] = {**record}

    sql_connection.fetch_none(filepath, query, parameters)


def delete(filepath: str, table: str, filter: models.Filter) -> None:
    """Delete a record from the database"""
    if not __table_exists(filepath, table):
        raise exceptions.TableNotFound(table)

    query: str = f"DELETE FROM {table} WHERE {filter}"

    sql_connection.fetch_none(filepath, query)


def fetch_types(filepath: str, table: str, fields: str) -> list[dict[str, str]]:
    """Fetch the types of a table"""
    fields_list = fields.lower().replace(", ", ",").split(",")

    fields = ", ".join([f"'{field}'" for field in fields_list])

    query: str = (
        f"SELECT name, type FROM pragma_table_info('{table}') WHERE name IN ({fields})"
    )

    records = sql_connection.fetch_all(filepath, query)

    fields_types: dict[str, str] = dict(
        zip([types["name"] for types in records], [types["type"] for types in records])
    )

    types: list[str] = []

    for field in fields_list:
        types.append(fields_types[field])  # if KeyError -> Invalid field

    return types


def __table_exists(filepath: str, table: str) -> bool:
    """Check if a table exists"""

    query = f"SELECT COUNT(1) FROM sqlite_master WHERE type='table' AND name='{table}'"

    return bool(sql_connection.fetch_one(filepath, query)[0]["COUNT(1)"])

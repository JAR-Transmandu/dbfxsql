import dbf
from contextlib import contextmanager
from typing import Any, Iterator

from dbf2sql_sync.common import utils


def fetch_all(query: str) -> list[dict[str, Any]]:
    """Executes a query returning all rows in the found set"""

    with __get_table() as table:
        # If there are records
        if values := table.query(query):
            return [dict(zip(table.field_names, value)) for value in values]

        return [{field: None for field in table.field_names}]


def fetch_one(query: str) -> list[dict[str, Any]] | None:
    """Executes a query returning one row in the found set"""

    with __get_table() as table:
        # If there are records
        if values := table.query(query)[0]:
            return [dict(zip(table.field_names, values))]

        return []


def fetch_none(query: str, parameters: dict[str, Any] | None = None) -> None:
    """Executes a query without returning values"""

    command: dict[str, Any] = {
        "CREATE": __create_table,
        "INSERT": __insert_record,
        "UPDATE": __update_record,
        "DELETE": __delete_record,
        "DROP": __drop_table,
    }

    with __get_table() as table:
        command[query](table, parameters) if parameters else command[query](table)


def __create_table(table: dbf.Table, parameters: str) -> None:
    table.add_fields(parameters)


def __insert_record(table: dbf.Table, parameters: dict[str, Any]) -> None:
    table.append(parameters)


def __update_record(table: dbf.Table, parameters: dict[str, Any]) -> None:
    with table.query(f"SELECT * WHERE id == {parameters["id"]}")[0] as record:
        for key, value in parameters.items():
            record[key] = value


def __delete_record(table: dbf.Table, parameters: str) -> None:
    with table.query(f"SELECT * WHERE id == {parameters["id"]}")[0] as record:
        dbf.delete(record)

    table.pack()


def __drop_table(table: dbf.Table) -> None:
    table.zap()
    table.delete_fields(table.field_names)


@contextmanager
def __get_table() -> Iterator[dbf.Table]:
    """Allows working with database table"""

    if utils.DBF_DATABASE.read_bytes():
        table: dbf.Table = dbf.Table(utils.DBF_DATABASE.as_posix()).open(dbf.READ_WRITE)
    else:
        table: dbf.Table = dbf.Table(utils.DBF_DATABASE.as_posix(), "id N(1,0)").open(
            dbf.READ_WRITE
        )

    try:
        yield table
    finally:
        table.close()

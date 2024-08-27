from . import sql_queries
from dbf2sql_sync.common import utils
from typing import Any


def insert_record(record: dict[str, Any]) -> None:
    sql_queries.insert(record)


def list_records() -> list[dict[str, Any]]:
    utils.show_table(records := sql_queries.list_all())

    return records


def detail_record(record: dict[str, Any]) -> dict[str, Any]:
    utils.show_table(record := sql_queries.details(record))

    return record


def update_record(record: dict[str, Any]) -> None:
    sql_queries.update(record)


def delete_record(record: dict[str, Any]) -> None:
    sql_queries.delete(record)


def reset_tables(fields: str) -> None:
    sql_queries.reset(fields)

from . import sql_queries
from typing import Any


def insert_record(record: dict[str, Any]) -> None:
    sql_queries.insert(record)


def list_records() -> list[dict[str, Any]]:
    return sql_queries.list_all()


def detail_record(record: dict[str, Any]) -> dict[str, Any]:
    return sql_queries.details(record)


def update_record(record: dict[str, Any]) -> None:
    sql_queries.update(record)


def delete_record(record: dict[str, Any]) -> None:
    sql_queries.delete(record)


def reset_tables(fields: str) -> None:
    sql_queries.reset(fields)

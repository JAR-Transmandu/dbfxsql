from . import dbf_queries
from typing import Any


def insert_record(data: dict[str, Any]) -> None:
    dbf_queries.insert(data)


def update_record(data: dict[str, Any]) -> None:
    dbf_queries.update(data)


def list_records() -> list[dict[str, Any]]:
    return dbf_queries.list_all()


def detail_record(data: dict[str, Any]) -> dict[str, Any]:
    return dbf_queries.details(data)


def delete_record(data: dict[str, Any]) -> None:
    dbf_queries.delete(data)


def reset_tables(fields: str) -> None:
    dbf_queries.reset(fields)

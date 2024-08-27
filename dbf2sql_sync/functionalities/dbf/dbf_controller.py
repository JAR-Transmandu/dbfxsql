from . import dbf_queries
from dbf2sql_sync.common import utils
from typing import Any


def insert_record(data: dict[str, Any]) -> None:
    dbf_queries.insert(data)


def update_record(data: dict[str, Any]) -> None:
    dbf_queries.update(data)


def list_records() -> list[dict[str, Any]]:
    return utils.format_dbf(dbf_queries.list_all())


def detail_record(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return utils.format_dbf(dbf_queries.details(data))


def delete_record(data: dict[str, Any]) -> None:
    dbf_queries.delete(data)


def reset_tables(fields: str) -> None:
    dbf_queries.reset(fields)

from dbf2sql_sync.common import utils
from dbf2sql_sync.common.exceptions import FileNotFound, RecordNotFound
from typing import Any
from . import dbf_connection


def insert_record(table: str, fields: str, values: str) -> None:
    filename: str = table + ".dbf"

    if not utils.file_exists(filename):
        raise FileNotFound(f"File not found: {filename}")

    record: dict[str, Any] = utils.format_data(fields, values)

    dbf_connection.insert(table, record)


def update_record(table: str, fields: str, values: str, condition: str) -> None:
    filepath: str = utils.generate_filepath(table)
    utils.validate_file(filepath)

    record: dict[str, Any] = utils.data_as_dict(fields, values)
    utils.validate_record(record)

    condition = utils.format_condition(condition)
    utils.validate_condition(condition)

    dbf_connection.update(table, record, condition)


def list_records(table: str) -> list[dict[str, Any]]:
    filename: str = table + ".dbf"
    if not utils.file_exists(filename):
        raise FileNotFound(f"File not found: {filename}")

    return utils.format_dbf(dbf_connection.list_all(filename))


def detail_record(table: str, condition: str) -> dict[str, Any]:
    filename: str = table + ".dbf"
    if not utils.file_exists(filename):
        raise FileNotFound(f"File not found: {filename}")

    condition = utils.format_condition(condition)

    record: dict[str, Any] | None = dbf_connection.detail(filename, condition)

    if not bool(record):
        raise RecordNotFound(f"No record with '{condition}'")

    return utils.format_dbf(record)


def delete_record(table: str, condition: str) -> None:
    filename: str = table + ".dbf"
    if not utils.file_exists(filename):
        raise FileNotFound(f"File not found: {filename}")

    condition = utils.format_condition(condition)
    if not detail_record(filename, condition):
        raise RecordNotFound(f"No record with '{condition}'")

    dbf_connection.delete(filename, condition)


def create_table(table: str, fields: str) -> None:
    filename: str = table + ".dbf"
    if not utils.file_exists(filename):
        utils.create_file(filename)

    dbf_connection.create(filename, fields)


def drop_table(table: str) -> None:
    filename: str = table + ".dbf"
    if not utils.file_exists(filename):
        raise FileNotFound(f"File not found: {filename}")

    # dbf_connection.drop(filename)
    utils.delete_file(filename)


# assing id

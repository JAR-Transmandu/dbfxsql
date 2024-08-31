"""Auxiliary tasks of the application"""

from pathlib import Path
from prettytable import PrettyTable
from dbf2sql_sync.common.exceptions import FileNotFound, RecordNotValid, RecordNotFound
from typing import Any

FOLDERPATH: Path = Path.cwd() / "dbf2sql_sync" / "common" / "databases"


def generate_filepath(filename: str) -> str:
    return str(FOLDERPATH / filename)


def validate_file(filename: str) -> None:
    path = FOLDERPATH / filename

    if not path.exists():
        raise FileNotFound(f"File not found: {filename}")


forma


def validate_record(record: dict[str, Any]) -> None:
    if not __fields_valid(record):
        raise RecordNotValid(f"Invalid fields record: {record}")

    if not __values_valid(record):
        raise RecordNotValid(f"Invalid values record: {record}")


def __fields_valid(record: dict[str, Any]) -> bool:
    return all(field in record for field in record.keys())

    if not record_valid(record):
        raise RecordNotValid(f"Invalid record: {record}")

    condition = utils.format_condition(condition)
    if not detail_record(filename, condition):
        raise RecordNotFound(f"No record with '{condition}'")


def create_file(filename: str) -> None:
    path = FOLDERPATH / filename

    path.touch()


def delete_file(filename: str) -> None:
    path = FOLDERPATH / filename

    path.unlink()


def format_condition(condition: str) -> str:
    """Transform the condition to uppercase"""

    condition = condition.strip().lower()

    if "=" in condition and ["!", ">", "<", "=="] not in condition:
        condition = condition.replace("=", "==")

    return condition


def format_data(headers: str, values: str) -> dict[str, Any]:
    """Transform the data to a dictionary"""

    headers_list = headers.lower().strip().split(",")
    values_list = values.lower().strip().split(",")

    return dict(zip(headers_list, values_list))


def file_exists(filename: str) -> bool:
    """Check if a file exists"""

    path = FOLDERPATH / filename

    return path.exists()


def format_dbf(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Transform the fields to lower case and strip the values"""

    # lower case fields
    lower_keys = [key.lower() for key in records[0].keys()]

    # strip values
    for record in records:
        for key in record.keys():
            record[key] = (
                record[key].rstrip() if isinstance(record[key], str) else record[key]
            )

    return [dict(zip(lower_keys, record.values())) for record in records]


def show_table(records: list[dict[str, Any]]) -> None:
    table = PrettyTable()

    table.field_names = records[0].keys() if records else []

    for record in records:
        table.add_row(
            [
                record[field] if isinstance(record[field], str) else str(record[field])
                for field in table.field_names
            ]
        )

    print(table, end="\n\n")


def reset_databases() -> None:
    """Delete the database and storage to create them again"""

    if DBF_DATABASE.exists() or SQL_DATABASE.exists():
        SQL_DATABASE.unlink()
        DBF_DATABASE.unlink()

    DBF_DATABASE.touch()
    SQL_DATABASE.touch()

from . import dbf_queries
from dbfxsql.common import file_manager, formatters, models, exceptions, utils


def create_table(table: str, fields: str) -> None:
    filepath: str = file_manager.generate_filepath(table, database="dbf")
    if file_manager.filepath_exists(filepath):
        raise exceptions.TableAlreadyExists(table)

    file_manager.create_file(filepath)
    dbf_queries.create(filepath, fields.lower())


def drop_table(table: str) -> None:
    filepath: str = file_manager.generate_filepath(table, database="dbf")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.FileNotFound(filepath)

    # dbf_queries.drop(filepath) ¯\(ツ)/¯
    file_manager.delete_file(filepath)


def add_fields(table: str, fields: str, increment: str = "") -> None:
    filepath: str = file_manager.generate_filepath(table, database="dbf")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.FileNotFound(filepath)

    increment = True if "True" == increment else False

    dbf_queries.add(filepath, fields.lower(), increment)

    # delete backup
    filepath: str = file_manager.generate_filepath(f"{table}_backup", database="dbf")
    if file_manager.filepath_exists(filepath):
        file_manager.delete_file(filepath)


def count_records(table: str) -> int:
    filepath: str = file_manager.generate_filepath(table, database="dbf")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.FileNotFound(filepath)

    return dbf_queries.count(filepath)


def insert_record(table: str, fields: str, values: str) -> None:
    filepath: str = file_manager.generate_filepath(table, database="dbf")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.FileNotFound(filepath)

    # assign types to each value
    types: dict[str, str] = dbf_queries.fetch_types(filepath, fields)
    record: dict[str, any] = formatters.format_input(fields, values, types)

    # check if other record have the same id
    if "id" in fields:
        records: list[dict[str, any]] = dbf_queries.read(filepath)
        records = formatters.format_output(records)

        if __record_exists(records, record):
            raise exceptions.RecordAlreadyExists(record["id"])

    dbf_queries.insert(filepath, record)


def read_records(table: str, condition: str | None = None) -> list[dict[str, any]]:
    filepath: str = file_manager.generate_filepath(table, database="dbf")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.FileNotFound(filepath)

    # assign types to each value
    records: list[dict[str, any]] = dbf_queries.read(filepath)
    records = formatters.format_output(records)

    # manual filter of records by condition
    if condition:
        filter: models.Filter = formatters.parse_condition(condition)

        if "id" == filter.field:
            records, _ = formatters.filter_records(records, filter, limit=1)
        else:
            records, _ = formatters.filter_records(records, filter)

    if not records:
        raise exceptions.RecordNotFound(condition)

    # utils.show_table(records)
    return records


def update_records(table: str, fields: str, values: str, condition: str) -> None:
    filepath: str = file_manager.generate_filepath(table, database="dbf")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.FileNotFound(filepath)

    # assign types to each value
    types: list[str] = dbf_queries.fetch_types(filepath, fields)
    record: dict[str, any] = formatters.format_input(fields, values, types)

    # get a sanitized list of records
    records: list[dict[str, any]] = dbf_queries.read(filepath)
    records = formatters.format_output(records)

    # check if other record have the same id
    if "id" in fields and __record_exists(records, record):
        raise exceptions.RecordAlreadyExists(record["id"])

    # manual filter of records by condition
    filter: models.Filter = formatters.parse_condition(condition)

    if "id" == filter.field:
        _, indexes = formatters.filter_records(records, filter, limit=1)
    else:
        _, indexes = formatters.filter_records(records, filter)

    if not indexes:
        raise exceptions.RecordNotFound(condition)

    # update filtered records by their index
    dbf_queries.update(filepath, record, indexes)


def delete_records(table: str, condition: str) -> None:
    filepath: str = file_manager.generate_filepath(table, database="dbf")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.FileNotFound(filepath)

    # get a sanitized list of records
    records: list[dict[str, any]] = dbf_queries.read(filepath)
    records = formatters.format_output(records)

    # manual filter of records by condition
    filter: models.Filter = formatters.parse_condition(condition)

    if "id" == filter.field:
        _, indexes = formatters.filter_records(records, filter, limit=1)
    else:
        _, indexes = formatters.filter_records(records, filter)

    if not indexes:
        raise exceptions.RecordNotFound(condition)

    # delete filtered records by their index
    dbf_queries.delete(filepath, indexes)


def __record_exists(records: list[dict[str, any]], record: dict[str, any]) -> bool:
    condition = f"id == {record['id']}"
    filter: models.Filter = formatters.parse_condition(condition)

    record, _ = formatters.filter_records(records, filter, limit=1)

    return bool(record)

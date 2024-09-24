from . import sql_queries
from dbfxsql.common import file_manager, formatters, models, exceptions


def create_database(db: str) -> None:
    filepath: str = file_manager.generate_filepath(db, database="sql")
    if file_manager.filepath_exists(filepath):
        raise exceptions.DatabaseAlreadyExists(db)

    file_manager.create_file(filepath)


def drop_database(db: str) -> None:
    filepath: str = file_manager.generate_filepath(db, database="sql")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.DatabaseNotFound(filepath)

    file_manager.delete_file(filepath)


def count_records(db: str, table: str) -> int:
    filepath: str = file_manager.generate_filepath(db, database="sql")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.DatabaseNotFound(filepath)

    return sql_queries.count(filepath, table)


def create_table(db: str, table: str, fields: str) -> None:
    filepath: str = file_manager.generate_filepath(db, database="sql")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.DatabaseNotFound(filepath)

    sql_queries.create(filepath, table, fields)


def drop_table(db: str, table: str) -> None:
    filepath: str = file_manager.generate_filepath(db, database="sql")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.DatabaseNotFound(filepath)

    sql_queries.drop(filepath, table)


def insert_record(db: str, table: str, fields: str, values: str) -> None:
    filepath: str = file_manager.generate_filepath(db, database="sql")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.DatabaseNotFound(filepath)

    types: dict[str, str] = sql_queries.fetch_types(filepath, table, fields)
    record: dict[str, any] = formatters.format_input(fields, values, types)

    if "id" in fields:
        filter: models.Filter = formatters.parse_condition(f"id == {record['id']}")

        if __record_exists(filepath, table, filter):
            raise exceptions.RecordAlreadyExists(record["id"])

    sql_queries.insert(filepath, table, record)


def read_records(
    db: str, table: str, condition: str | None = None
) -> list[dict[str, any]]:
    filepath: str = file_manager.generate_filepath(db, database="sql")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.DatabaseNotFound(filepath)

    if condition:
        filter: models.Filter = formatters.parse_condition(condition)

        if not __record_exists(filepath, table, filter):
            raise exceptions.RecordNotFound(condition)

        records: list[dict[str, any]] = sql_queries.read(filepath, table, filter)
    else:
        records: list[dict[str, any]] = sql_queries.read(filepath, table)

    return records


def update_records(
    db: str, table: str, fields: str, values: str, condition: str
) -> None:
    filepath: str = file_manager.generate_filepath(db, database="sql")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.DatabaseNotFound(filepath)

    types: dict[str, str] = sql_queries.fetch_types(filepath, table, fields)
    record: dict[str, any] = formatters.format_input(fields, values, types)

    # check if other record have the same id
    if "id" in fields:
        filter: models.Filter = formatters.parse_condition(f"id == {record['id']}")

        if __record_exists(filepath, table, filter):
            raise exceptions.RecordAlreadyExists(record["id"])

    # check if this record exists
    filter: models.Filter = formatters.parse_condition(condition)

    if not __record_exists(filepath, table, filter):
        raise exceptions.RecordNotFound(condition)

    sql_queries.update(filepath, table, record, filter)


def delete_records(db: str, table: str, condition: str) -> None:
    filepath: str = file_manager.generate_filepath(db, database="sql")
    if not file_manager.filepath_exists(filepath):
        raise exceptions.DatabaseNotFound(filepath)

    filter: models.Filter = formatters.parse_condition(condition)

    if not __record_exists(filepath, table, filter):
        raise exceptions.RecordNotFound(condition)

    sql_queries.delete(filepath, table, filter)


def __record_exists(filepath: str, table: str, filter: models.Filter) -> bool:
    records: list[dict[str, any]] = sql_queries.read(filepath, table, filter)

    return bool(formatters.depurate_empty_records(records))

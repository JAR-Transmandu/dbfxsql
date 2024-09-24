from dbfxsql.common import file_manager
from dbfxsql.functionalities import dbf_controller, sql_controller


def insert_record(origin: dict, destiny: dict, record: dict) -> None:
    file: str = destiny["file"]
    table: str = destiny["table"]
    fields: str = ", ".join(destiny["fields"])
    values: str = ", ".join([str(record[field]) for field in origin["fields"]])

    if file.endswith(".dbf"):
        dbf_controller.insert_record(table, fields, values)
    else:
        database, _ = file_manager.decompose_filename(file)
        sql_controller.insert_record(database, table, fields, values)


def read_records(filename: str, table: str) -> dict:
    if filename.endswith(".dbf"):
        return dbf_controller.read_records(table)

    database, _ = file_manager.decompose_filename(filename)
    return sql_controller.read_records(database, table)


def update_record(destiny: dict, origin: dict, record: dict) -> None:
    file: str = destiny["file"]
    table: str = destiny["table"]
    fields: str = ", ".join(destiny["fields"])
    values: str = ", ".join([str(record[field]) for field in origin["fields"]])
    condition: str = f"id == {record['id']}"

    if file.endswith(".dbf"):
        dbf_controller.update_records(table, fields, values, condition)
    else:
        database, _ = file_manager.decompose_filename(file)
        sql_controller.update_records(database, table, fields, values, condition)


def delete_record(destiny: dict, record: dict) -> None:
    file: str = destiny["file"]
    table: str = destiny["table"]
    condition: str = f"id == {record['id']}"

    if file.endswith(".dbf"):
        dbf_controller.delete_records(table, condition)
    else:
        database, _ = file_manager.decompose_filename(file)
        sql_controller.delete_records(database, table, condition)

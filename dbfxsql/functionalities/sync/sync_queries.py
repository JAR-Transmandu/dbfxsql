from dbfxsql.common import file_manager, formatters
from dbfxsql.functionalities import dbf_controller, sql_controller


def get_origin(relations: list[dict[str, list[str]]], filename: str) -> dict:
    table: str = formatters.get_table(relations, filename)

    return {
        "file": filename,
        "table": table,
        "fields": [],
        "records": __read(filename, table),
    }


def parse_relation(relation: dict, origin: dict) -> dict:
    destiny: dict = {"file": "", "table": "", "fields": [], "records": []}

    for (
        index,
        (file, table),
    ) in enumerate(zip(relation["files"], relation["tables"])):
        if file == origin["file"] and table == origin["table"]:
            origin["fields"] = relation["fields"][index].split(", ")

        else:
            destiny["file"] = file
            destiny["table"] = table
            destiny["fields"] = relation["fields"][index].split(", ")
            destiny["records"] = __read(file, table)

    return origin, destiny


def update_record(destiny: dict, origin: dict, record: dict) -> None:
    file: str = destiny["file"]
    table: str = destiny["table"]
    fields: str = ", ".join(destiny["fields"])
    values: str = ", ".join([str(record[field]) for field in origin["fields"]])
    condition: str = f"id == {record['id']}"

    if file.endswith(".dbf"):
        dbf_controller.update_records(table, fields, values)
        return

    database, _ = file_manager.decompose_file(file)
    sql_controller.update_records(database, table, fields, values, condition)


def insert_record(origin: dict, destiny: dict, record: dict) -> None:
    file: str = destiny["file"]
    table: str = destiny["table"]
    fields: str = ", ".join(destiny["fields"])
    values: str = ", ".join([str(record[field]) for field in origin["fields"]])

    if file.endswith(".dbf"):
        dbf_controller.insert_record(table, fields, values)
        return

    database, _ = file_manager.decompose_file(file)
    sql_controller.insert_record(database, table, fields, values)


def delete_record(destiny: dict, record: dict) -> None:
    file: str = destiny["file"]
    table: str = destiny["table"]
    condition: str = f"id == {record['id']}"

    if file.endswith(".dbf"):
        dbf_controller.delete_records(table, condition)
        return

    database, _ = file_manager.decompose_file(file)
    sql_controller.delete_records(database, table, condition)


def __read(file, table) -> list[dict]:
    if file.endswith(".dbf"):
        return dbf_controller.read_records(table)

    database, _ = file_manager.decompose_file(file)
    return sql_controller.read_records(database, table)

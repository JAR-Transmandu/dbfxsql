from dbfxsql.common import file_manager
from dbfxsql.functionalities import dbf_controller, sql_controller


def read_records(relations: list[dict]) -> list[list[dict]]:
    grouped_data: list = []

    for relation in relations:
        data: list = []

        for file, table in zip(relation["files"], relation["tables"]):
            if file.endswith(".dbf"):
                records = dbf_controller.read_records(table)

            else:
                database, _ = file_manager.decompose_file(file)
                records = sql_controller.read_records(database, table)

            data.append({str(file): {str(table): records}})
        grouped_data.append(data)

    return grouped_data


def insert_record() -> None:
    raise NotImplementedError


def update_record() -> None:
    raise NotImplementedError


def delete_record() -> None:
    raise NotImplementedError

from . import sync_connection
from dbfxsql.common import formatters


def data_asdict(file: str, table: str) -> list:
    data: dict = {
        "file": file,
        "table": table,
        "records": sync_connection.read_records(file, table),
    }

    return data


def parse_relation(relation: dict, modified_data: list) -> dict:
    """Parses a relation and returns the origin and destiny dictionaries."""

    origin: dict = {"file": "", "table": "", "fields": [], "records": []}
    destiny: dict = {"file": "", "table": "", "fields": [], "records": []}

    for (
        index,
        (file, table),
    ) in enumerate(zip(relation["files"], relation["tables"])):
        if file == modified_data["file"] and table == modified_data["table"]:
            origin["file"] = file
            origin["table"] = table
            origin["fields"] = relation["fields"][index].split(", ")
            origin["records"] = modified_data["records"][:]

        else:
            destiny["file"] = file
            destiny["table"] = table
            destiny["fields"] = relation["fields"][index].split(", ")
            destiny["records"] = sync_connection.read_records(file, table)

    return origin, destiny


def operator(origin: dict[str, any], destiny: dict[str, any]) -> None:
    """Performs the synchronization process."""

    origin["records"] = formatters.depurate_empty_records(origin["records"])
    destiny["records"] = formatters.depurate_empty_records(destiny["records"])

    if origin["records"] == destiny["records"]:
        return

    residual_origin: list = origin["records"][:]
    residual_destiny: list = destiny["records"][:]

    # update matching records
    for origin_record in origin["records"]:
        for destiny_record in destiny["records"]:
            if origin_record["id"] == destiny_record["id"]:
                comparator(origin, destiny, origin_record, destiny_record)

                residual_origin.remove(origin_record)
                residual_destiny.remove(destiny_record)
                break

    # insert residual origin records
    for origin_record in residual_origin:
        print(f"Insert in {destiny["file"]}: {origin_record}")
        sync_connection.insert_record(origin, destiny, origin_record)

    # delete residual destiny records
    for destiny_record in residual_destiny:
        print(f"Delete in {destiny["file"]}: {destiny_record}")
        sync_connection.delete_record(destiny, destiny_record)


def comparator(
    origin: dict, destiny: dict, origin_record: dict, destiny_record: dict
) -> None:
    """Compares the origin and destiny records and updates if necessary."""

    for index, (origin_field, destiny_field) in enumerate(
        zip(origin["fields"], destiny["fields"])
    ):
        if origin_record[origin_field] != destiny_record[destiny_field]:
            origin["fields"].remove("id")
            destiny["fields"].remove("id")

            sync_connection.update_record(destiny, origin, origin_record)

            break

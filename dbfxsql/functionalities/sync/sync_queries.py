from . import sync_connection
from dbfxsql.common import formatters


def parse_relation(relation: dict, data: list) -> dict:
    """Parses a relation and returns the origin and destiny dictionaries."""

    origin: dict = {"file": "", "table": "", "fields": [], "records": []}
    destiny: dict = {"file": "", "table": "", "fields": [], "records": []}

    for (
        index,
        (file, table),
    ) in enumerate(zip(relation["files"], relation["tables"])):
        if file == data[0] and table == data[1]:
            origin["file"] = file
            origin["table"] = table
            origin["fields"] = relation["fields"][index].split(", ")
            origin["records"] = data[2][:]

        else:
            destiny["file"] = file
            destiny["table"] = table
            destiny["fields"] = relation["fields"][index].split(", ")
            destiny["records"] = sync_connection.read_records(file, table)

    return origin, destiny


def operator(origin: dict[str, any], destiny: dict[str, any]) -> None:
    """Performs the synchronization process."""

    origin["records"] = formatters.depurate_empty_tables(origin["records"])
    destiny["records"] = formatters.depurate_empty_tables(destiny["records"])

    if origin["records"] == destiny["records"]:
        return

    # update matching records
    for origin_record in origin["records"]:
        for destiny_record in destiny["records"]:
            if origin_record["id"] == destiny_record["id"]:
                comparator(origin, destiny, origin_record, destiny_record)

                origin["records"].remove(origin_record)
                destiny["records"].remove(destiny_record)

    # insert residual origin records
    for origin_record in origin["records"]:
        print(f"Insert: {origin_record}")
        sync_connection.insert_record(origin, destiny, origin_record)

    # delete residual destiny records
    for destiny_record in destiny["records"]:
        print(f"Delete: {destiny_record}")
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

            print(f"{origin_field} -> {destiny_field}")
            sync_connection.update_record(destiny, origin, origin_record)

            return

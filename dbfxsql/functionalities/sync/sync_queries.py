from dbfxsql.common import formatters, file_manager
from . import sync_connection


def operator(origin: dict[str, any], destiny: dict[str, any]) -> None:
    # no changes
    if origin["records"] == destiny["records"]:
        return

    # empty tables
    origin["records"] = formatters.depurate_empty_tables(origin["records"])
    destiny["records"] = formatters.depurate_empty_tables(destiny["records"])

    print(f"\nOrigin: {origin["records"]}\nDestiny: {destiny["records"]}\n")

    # update
    for origin_record in origin["records"]:
        for destiny_record in destiny["records"]:
            if origin_record["id"] == destiny_record["id"]:
                comparator(origin, destiny, origin_record, destiny_record)

                origin["records"].remove(origin_record)
                destiny["records"].remove(destiny_record)

    # insert
    for origin_record in origin["records"]:
        print(f"Insert: {origin_record}")
        sync_connection.insert_record(origin, destiny, origin_record)

    # delete
    for destiny_record in destiny["records"]:
        print(f"Delete: {destiny_record}")
        sync_queries.delete_record(destiny, destiny_record)


def comparator(
    origin: dict, destiny: dict, origin_record: dict, destiny_record: dict
) -> None:
    for index, (origin_field, destiny_field) in enumerate(
        zip(origin["fields"], destiny["fields"])
    ):
        if origin_record[origin_field] != destiny_record[destiny_field]:
            origin["fields"].remove("id")
            destiny["fields"].remove("id")

            print(f"{origin_field} -> {destiny_field}")
            sync_queries.update_record(destiny, origin, origin_record)

            return

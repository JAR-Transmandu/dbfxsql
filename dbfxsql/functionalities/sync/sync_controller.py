import logging
import json
import asyncio
import os
from yaspin import yaspin
from decouple import config
from watchfiles import arun_process

from . import sync_queries
from dbfxsql.common import models, formatters, file_manager

# silent the watchfiles logger
logging.getLogger("watchfiles").setLevel(logging.ERROR)


def main() -> None:
    with yaspin(color="cyan", timer=True) as spinner:
        try:
            spinner.text = "Initializing..."
            spinner.text = "Listening..."

            # asyncio.run(listener())
            runner()

        except KeyboardInterrupt:
            spinner.ok("END")


async def listener() -> None:
    await arun_process(
        config("DBF_FOLDERPATH"),
        config("SQL_FOLDERPATH"),
        target=runner,
        watch_filter=models.Watcher(),
    )


def runner() -> None:
    # filename: str =
    if not (filename := "usuarios.sql"):
        return

    if not (relations := formatters.filter_relations(filename)):
        return

    table = formatters.get_table(relations, filename)
    records = sync_queries.read_records(filename, table)

    for relation in relations:
        origin, destiny = sync_queries.parse_relation(
            relation, [filename, table, records]
        )
        operator(origin, destiny)


def depurator() -> str:
    if not (changes := json.loads(os.getenv("WATCHFILES_CHANGES"))):
        return

    filepath: str = changes.pop()[-1]  # ignore the event, take the file name
    name, extension = file_manager.decompose_file(filepath)

    filename: str = f"{name}.{extension}"

    return filename


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
        sync_queries.insert_record(origin, destiny, origin_record)

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

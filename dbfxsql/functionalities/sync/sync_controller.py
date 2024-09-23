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

            asyncio.run(listener())

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
    filename: str = depurator()

    if not filename or filename.endswith(".sql"):
        return

    relations: list[dict[str, list[str]]] = formatters.filter_relations(filename)

    if not relations:
        return

    origin = sync_queries.get_origin(relations, filename)

    for relation in relations:
        origin, destiny = sync_queries.parse_relation(relation, origin)

        operator(origin, destiny)


def depurator() -> str:
    changes: list[list[str]] = os.getenv("WATCHFILES_CHANGES")

    if changes == "[]":
        return

    changes = json.loads(changes)

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

    # update
    for origin_record in origin["records"]:
        for destiny_record in destiny["records"]:
            if origin_record["id"] == destiny_record["id"]:
                comparator(origin, destiny, origin_record, destiny_record)

            origin["records"].remove(origin_record)
            destiny["records"].remove(destiny_record)

    # insert
    for origin_record in origin["records"]:
        sync_queries.insert_record(origin, destiny, origin_record)

    # delete
    for destiny_record in destiny["records"]:
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

            sync_queries.update_record(destiny, origin, origin_record)

            return

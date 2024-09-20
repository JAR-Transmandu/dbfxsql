import json
from yaspin import yaspin
from decouple import config
from watchfiles import watch
from pprint import pprint
from contextlib import contextmanager

from . import sync_queries
from dbfxsql.common import file_manager, models, formatters


def main() -> None:
    with yaspin(color="cyan", timer=True) as spinner:
        try:
            spinner.text = "Initializing..."
            spinner.text = "Listening..."

            with listener() as filename:
                runner(filename)

        except KeyboardInterrupt:
            spinner.ok("END")


@contextmanager
def listener() -> None:
    dbf_folder: str = config("DBF_FOLDERPATH")
    sql_folder: str = config("SQL_FOLDERPATH")
    for changes in watch(dbf_folder, sql_folder, watch_filter=models.Watcher()):
        filename: str = changes.pop()[-1]  # ignore the event, take the file name

        yield filename


def runner(filename: str) -> None:
    relations: list[dict[str, list[str]]] = formatters.filter_relations(filename)

    if not relations:
        return

    origin = sync_queries.get_origin(relations, filename)

    for relation in relations:
        origin, destiny = sync_queries.parse_relation(relation, origin)

        operator(origin, destiny)


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
    if origin_record["id"] == destiny_record["id"]:
        for index, (origin_field, destiny_field) in enumerate(
            zip(origin["fields"], destiny["fields"])
        ):
            if origin_record[origin_field] != destiny_record[destiny_field]:
                origin["fields"].remove("id")
                destiny["fields"].remove("id")

                sync_queries.update_record(destiny, origin, origin_record)

                return

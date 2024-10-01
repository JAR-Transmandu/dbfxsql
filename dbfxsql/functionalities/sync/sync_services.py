from . import sync_connection
from dbfxsql.common import formatters, utils, models
from typing import AsyncGenerator
from watchfiles import awatch


async def listen(folders: tuple[str]) -> AsyncGenerator[tuple, None]:
    """Asynchronously listens for file changes and triggers the runner function."""

    async for changes in awatch(*folders, watch_filter=utils.only_modified):
        yield formatters.parse_filepaths(changes)


def relevant_changes(filenames: list[str], relations: list[dict]) -> list[dict]:
    """Collects data from the files and returns it as a list of dictionaries."""
    changes: list = []

    for filename in filenames:
        origin: models.Actor = None
        destinies: list = []

        for relation in relations:
            if filename in relation["files"]:
                # send origin to save the object and only append the fields
                origin, destiny = _parse_actors(filename, relation, origin)
                destinies.append(destiny)

        changes.append({"origin": origin, "destinies": destinies})

    return changes


def classify(origin: models.Actor, destiny: models.Actor) -> tuple[list, list, list]:
    """Classifies changes into insert, update and delete operations."""

    insert: list = origin.records[:]  # a copy
    update: list = []
    delete: list = destiny.records[:]  # a copy

    fields: tuple = formatters.package_fields(origin, destiny)

    for origin_record in formatters.depurate_empty_records(origin.records):
        for destiny_record in formatters.depurate_empty_records(destiny.records):
            if origin_record["id"] == destiny_record["id"]:
                if change := _comparator(origin_record, destiny_record, fields):
                    update.append(change)

                insert.remove(origin_record)
                delete.remove(destiny_record)

    return insert, update, delete


def operate(insert: list, update: list, delete: list, header: dict) -> None:
    """Executes insert, update and delete operations."""
    for record in insert:
        sync_connection.insert(
            header["file"],
            header["table"],
            header["destiny_fields"],
            ", ".join(f"{record[field]}" for field in header["origin_fields"]),
        )

    for record in update:
        # avoid RecordAlreadyExists error
        header["origin_fields"].remove("id")
        header["destiny_fields"] = header["destiny_fields"].split(", ")
        header["destiny_fields"].remove("id")

        sync_connection.update(
            header["file"],
            header["table"],
            ", ".join(header["destiny_fields"]),
            ", ".join(f"{record[field]}" for field in header["origin_fields"]),
            f"id == {record['id']}",
        )

    for record in delete:
        sync_connection.delete(header["file"], header["table"], f"id == {record['id']}")


def _parse_actors(filename: str, relation: dict, origin: models.Actor | None) -> tuple:
    for index, file in enumerate(relation["files"]):
        if filename == file:
            if not origin:
                origin: models.Actor = __create_actor(relation, index)

            else:
                origin.fields.append(relation["fields"][index])

        else:
            destiny: models.Actor = __create_actor(relation, index)

    return origin, destiny


def _comparator(origin: dict, destiny: dict, fields: tuple) -> dict | None:
    for origin_field, destiny_field in fields:
        if origin[origin_field] != destiny[destiny_field]:
            return origin


def __create_actor(relation: dict, index: int) -> models.Actor:
    file: str = relation["files"][index]
    table: str = relation["tables"][index]
    fields: list[str] = [relation["fields"][index]]
    records: list[dict[str, any]] = sync_connection.read(file, table)

    return models.Actor(file=file, table=table, fields=fields, records=records)

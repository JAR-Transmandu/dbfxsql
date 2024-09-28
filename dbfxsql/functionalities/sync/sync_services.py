from . import sync_connection
from dbfxsql.common import formatters, utils, file_manager, models
from typing import AsyncGenerator
from watchfiles import awatch


async def listen(folders: tuple[str]) -> AsyncGenerator[tuple, None]:
    """Asynchronously listens for file changes and triggers the runner function."""

    async for changes in awatch(*folders, watch_filter=utils.only_modified):
        yield formatters.parse_filepaths(changes)


def relevant_changes(filenames: list[str], relations: list[dict]) -> list[dict]:
    """Collects data from the files and returns it as a list of dictionaries."""
    changes: list = []
    origin: list = []
    destinies: list = []

    for filename in filenames:
        for relation in relations:
            if filename in relation["files"]:
                origin, destiny = _parse_actors(filename, relation, origin)
                destinies.append(destiny)

    return changes


def _relevant_filenames(filenames: list[str]) -> list[str]:
    return filenames


def _parse_actors(filename: str, relation: dict, origin: list) -> tuple:
    destinies: list = []

    for index, file in enumerate(relation["files"]):
        if filename == file:
            if not origin:
                origin.append(__create_actor(relation, index))

            else:
                origin[0].fields.append(relation["fields"][index])

        else:
            destinies.append(__create_actor(relation, index))

    return origin, destinies


def __create_actor(relation: dict, index: int) -> models.Actor:
    file: str = relation["files"][index]
    table: str = relation["tables"][index]
    fields: list[str] = [relation["fields"][index]]
    records: list[dict[str, any]] = sync_connection.read_records(file, table)

    return models.Actor(file=file, table=table, fields=fields, records=records)

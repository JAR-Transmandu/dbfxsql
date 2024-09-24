import logging
from decouple import config
from watchfiles import arun_process

from . import sync_queries
from dbfxsql.common import models, formatters


def init() -> None:
    # silent the watchfiles logger
    logging.getLogger("watchfiles").setLevel(logging.ERROR)


async def listener() -> None:
    await arun_process(
        config("DBF_FOLDERPATH"),
        config("SQL_FOLDERPATH"),
        target=runner,
        watch_filter=models.Watcher(),
    )


def runner() -> None:
    file: str = "usuarios.sql"  # formatters.get_modified_file()
    relations: list[dict] = formatters.filter_relations(file)

    if not relations:
        return

    # get the tables and their records from the modified file
    table: str = formatters.get_table(relations, file)
    records: list[dict] = sync_queries.read_records(file, table)

    # compare the modified file with each table relationed
    for relation in relations:
        origin, destiny = sync_queries.parse_relation(relation, [file, table, records])
        sync_queries.operator(origin, destiny)

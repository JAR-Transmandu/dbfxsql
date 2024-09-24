import logging
from decouple import config
from watchfiles import arun_process

from . import sync_queries
from dbfxsql.common import models, formatters


def init() -> None:
    """Initializes the logger to suppress watchfiles logs."""

    logging.getLogger("watchfiles").setLevel(logging.ERROR)


async def listener() -> None:
    """Asynchronously listens for file changes and triggers the runner function."""

    await arun_process(
        config("DBF_FOLDERPATH"),
        config("SQL_FOLDERPATH"),
        target=runner,
        watch_filter=models.Watcher(),
    )


def runner() -> None:
    """Runs the synchronization process."""

    # get the modified file
    modified_file: str = "usuarios.sql"  # formatters.get_modified_file()
    if not modified_file:
        return

    # get the relations from the modified file
    relations: list[dict] = formatters.filter_relations(modified_file)
    if not relations:
        return

    modified_data: dict = {
        "file": modified_file,
        "table": formatters.get_table(relations, modified_file),
        "records": sync_queries.read_records(
            modified_file, formatters.get_table(relations, modified_file)
        ),
    }

    # compare the modified data with each table relationed
    for relation in relations:
        origin, destiny = sync_queries.parse_relation(relation, modified_data)
        sync_queries.operator(origin, destiny)

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
    modified_files: list = formatters.get_modified_files()
    if not modified_files:
        return

    relevant_data: list[dict, ...] = formatters.parse_by_relations(modified_files)
    if not relevant_data:
        return

    relevant_data: list = []
    for files in modified_files:
        # get origin

        for data in relevant_data:
            print(data)


def foo() -> None:
    """Runs the synchronization process."""

    # get the modified file
    modified_files: list = formatters.get_modified_files()
    if not modified_files:
        return

    # get the relations from the modified file
    for file in modified_files:
        relations: list[dict] = formatters.filter_relations(file)
        if not relations:
            return

    modified_tables: list[str] = formatters.get_tables(relations, modified_file)

    # read all tables of the modified file
    for modified_table in modified_tables:
        modified_data: dict = sync_queries.data_asdict(modified_file, modified_table)

        # compare the modified data with each table relationed
        for relation in relations:
            origin, destiny = sync_queries.parse_relation(relation, modified_data)
            sync_queries.operator(origin, destiny)

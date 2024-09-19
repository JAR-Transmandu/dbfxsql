from yaspin import yaspin
from decouple import config
from watchfiles import watch

from . import sync_queries
from dbfxsql.common import file_manager, models, formatters

from contextlib import contextmanager
from collections.abc import Generator


def main() -> None:
    # with yaspin(color="cyan", timer=True) as spinner:
    # try:
    #    spinner.text = "Initializing..."
    #     file_manager.rewrite_pool()

    #     spinner.text = "Listening..."

    with listener() as data:
        comparator(data)


# except KeyboardInterrupt:
#     spinner.ok("END")


@contextmanager
def listener() -> Generator[list[list[dict]]]:
    try:
        #   for changes in watch(
        # config("DBF_FOLDERPATH"),
        # config("SQL_FOLDERPATH"),
        # watch_filter=models.Watcher(),
        # ):
        # filename: str = changes.pop()[-1]  # ignore the event, take the file name
        filename: str = "users.dbf"

        relations: list[dict] = formatters.filter_relations(filename)
        data: list[list[dict]] = sync_queries.read(relations)

        yield data

    except Exception as error:
        print(error)


def comparator(data: list[list[dict]]) -> None:
    for relations in data:
        print(relations)

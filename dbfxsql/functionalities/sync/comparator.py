import json
from watchfiles import watch

from dbfxsql.common import models, utils


def comparator() -> None:
    for changes in watch(
        contants.POOL,
        watch_filter=models.Watcher(),
    ):
        with open(contants.POOL, "r") as file:
            data = json.loads(file.read())

            print(data)


def main() -> None:
    comparator()

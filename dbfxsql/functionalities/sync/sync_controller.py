import logging
from decouple import config
from dbfxsql.common import models

from . import sync_services
from dbfxsql.common import file_manager, formatters, utils


def init() -> None:
    logging.getLogger("watchfiles").setLevel(logging.ERROR)

    setup: dict[str, any] = file_manager.load_toml()
    setup["folders"]: tuple[str] = (config("DBF_FOLDERPATH"), config("SQL_FOLDERPATH"))

    return setup


async def synchronize(setup: list[list[dict]]) -> None:
    folders: tuple[str] = setup["folders"]
    relations: list[dict] = setup["relations"]

    async for filenames in sync_services.listen(folders):
        for change in sync_services.relevant_changes(filenames, relations):
            origin: models.Actor = change["origin"]

            print(origin.file)

            for index, destiny in enumerate(change["destinies"]):
                # copy with only the correspond fie
                _origin: models.Actor = utils.clone_actor(origin, index)

                insert, update, delete = sync_services.classify(_origin, destiny)

                # data to know where do the changes
                header: dict = _parse_header(_origin, destiny)

                utils.notify(insert, update, delete, header)

                sync_services.operate(insert, update, delete, header)


def _parse_header(origin: models.Actor, destiny: models.Actor) -> dict:
    return {
        "file": destiny.file,
        "table": destiny.table,
        "origin_fields": origin.fields[0].split(", "),
        "destiny_fields": destiny.fields[0],
    }

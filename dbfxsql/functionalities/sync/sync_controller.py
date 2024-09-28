import logging
from decouple import config

from . import sync_services
from dbfxsql.common import file_manager


def init() -> None:
    logging.getLogger("watchfiles").setLevel(logging.ERROR)

    return file_manager.load_toml()


async def synchronize(_config: list[list[dict]]) -> None:
    folders: tuple[str] = (config("DBF_FOLDERPATH"), config("SQL_FOLDERPATH"))
    relations: list[dict] = _config["relations"]

    async for filenames in sync_services.listen(folders):
        for change in sync_services.relevant_changes(filenames, relations):
            print(change)

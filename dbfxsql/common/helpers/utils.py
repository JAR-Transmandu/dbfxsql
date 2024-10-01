from prettytable import PrettyTable
from watchfiles import Change
from dbfxsql.common import models


def show_table(records: list[dict[str, any]]) -> None:
    """Displays a list of records in a table format."""

    table = PrettyTable()

    table.field_names = records[0].keys() if records else []

    for record in records:
        table.add_row([record[field] for field in table.field_names])

    print(table, end="\n\n")


def only_modified(change: Change, path: str) -> bool:
    allowed_extensions: tuple[str] = (".dbf", ".sql")

    return change == Change.modified and path.endswith(allowed_extensions)


def clone_actor(actor: models.Actor, index: int) -> models.Actor:
    return models.Actor(
        file=actor.file,
        table=actor.table,
        fields=[actor.fields[index]],
        records=actor.records[:],
    )

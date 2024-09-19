"""Auxiliary tasks of the application"""

from prettytable import PrettyTable


def show_table(records: list[dict[str, any]]) -> None:
    table = PrettyTable()

    table.field_names = records[0].keys() if records else []

    for record in records:
        table.add_row(
            [record[field] if record[field] else None for field in table.field_names]
        )

    print(table, end="\n\n")

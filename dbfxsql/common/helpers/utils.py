from prettytable import PrettyTable


def show_table(records: list[dict[str, any]]) -> None:
    """Displays a list of records in a table format."""

    table = PrettyTable()

    table.field_names = records[0].keys() if records else []

    for record in records:
        table.add_row([record[field] for field in table.field_names])

    print(table, end="\n\n")

"""Database management for the table"""

import dbf

from .dbf_connection import get_table


def create(filepath: str, fields: str) -> None:
    with get_table(filepath) as table:
        table.add_fields(fields)


def drop(filepath: str) -> None:
    with get_table(filepath) as table:
        table.zap()
        table.delete_fields(table.field_names)


def add(filepath: str, fields: str, increment: bool) -> None:
    with get_table(filepath) as table:
        table.add_fields(fields)

        if "id" in fields and increment:
            for i, _ in enumerate(table):
                with table[i] as row:
                    row["id"] = i + 1


def count(filepath: str) -> int:
    with get_table(filepath) as table:
        return table.field_count


def insert(filepath: str, record: dict[str, any]) -> None:
    with get_table(filepath) as table:
        table.append(record)


def read(filepath: str) -> list[dict[str, any]]:
    with get_table(filepath) as table:
        field_names: list[str] = [field.lower() for field in table.field_names]

        records: list[dict[str, any]] = [
            dict(zip(field_names, record)) for record in table
        ]

    return records if records else [{field: "" for field in field_names}]


def update(filepath: str, record: dict[str, any], indexes: list[int]) -> None:
    with get_table(filepath) as table:
        for index in indexes:
            with table[index] as row:
                for key, value in record.items():
                    setattr(row, key, value)


def delete(filepath: str, indexes: list[int]) -> None:
    with get_table(filepath) as table:
        for index in indexes:
            with table[index] as row:
                dbf.delete(row)

        table.pack()


def fetch_types(filepath: str, fields: str) -> list[str]:
    fields_list: list[str] = fields.lower().replace(", ", ",").split(",")
    names: list[str] = []
    types: list[str] = []
    _types: list[str] = []

    with get_table(filepath) as table:
        for i in range(table.field_count):
            names.append(table._field_layout(i).lower().split(" ")[0])
            _types.append(table._field_layout(i).split(" ")[-1][0])

        fields_types: dict[str, str] = dict(zip(names, _types))

        for field in fields_list:
            types.append(fields_types[field])

        return types

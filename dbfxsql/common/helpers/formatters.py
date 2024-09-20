import decimal
from . import file_manager
from ..entities import constants, models, exceptions


def format_input(fields: str, values: str, types: list[str]) -> dict[str, any]:
    record: dict[str, any] = __record_asdict(fields, values)

    for field, value, _type in zip(record.keys(), record.values(), types):
        record[field] = __assign_type(field, value, _type)

    return record


def format_output(records: list[dict[str, any]]) -> list[dict[str, any]]:
    """Transform the fields to lower case and strip the values"""

    # lower case fields
    lower_keys = [key.lower() for key in records[0].keys()]

    # strip values
    for record in records:
        for key in record.keys():
            record[key] = (
                record[key].rstrip() if isinstance(record[key], str) else record[key]
            )

    return [dict(zip(lower_keys, record.values())) for record in records]


def parse_condition(condition: str) -> models.Filter:
    parameters: list[str] = condition.split(" ")

    if 2 < len(parameters):
        for parameter in parameters[3:]:
            parameters[2] += " " + parameter

    filter: models.Filter = models.Filter(
        field=parameters[0], operator=parameters[1], value=parameters[2]
    )

    if "=" == filter.operator:
        filter.operator += "="

    return filter


def filter_records(
    _records: list[dict[str, any]], filter: models.Filter, limit: int = -1
) -> tuple[list[dict[str, any]], list[int]]:
    records: list[any] = []
    indexes: list[any] = []
    count: int = 0

    for index, record in enumerate(_records):
        condition: str = f"'{record[filter.field]}'{filter.operator}"

        # force SQL format - users should write ' with strings
        if isinstance(record[filter.field], str):
            condition += f"'{filter.value}'"
        else:
            condition += f"{filter.value}"

        if eval(condition) and count != limit:
            records.append(record)
            indexes.append(index)

            count -= -1  # count++

    return records, indexes


def depurate_empty_tables(records: list[dict]) -> list:
    if not records:
        return records

    records_set = [{record for record in records.values()} for records in records]

    # if records_set is empty then update records
    if 1 == len(records_set) and not records_set[0]:
        return []

    return records


def get_table(relations: list[dict[str, list[str]]], filename: str) -> tuple:
    for relation in relations:
        for index, file in enumerate(relation["files"]):
            if filename == file:
                return relation["tables"][index]


def filter_relations(filename: str) -> list[dict[str, any]]:
    relations: list[dict] = file_manager.load_toml()["relations"]

    return [relation for relation in relations if filename in relation["files"]]


def __assign_type(field, value: str, _type: str) -> any:
    try:
        if "L" == _type and ("True" != value != "False"):
            raise exceptions.ValueNotValid(value, field, "bool")

        if "D" == _type or "@" == _type:
            value.replace("/", "-")

        _types = constants.DBF if _type in constants.DBF.keys() else constants.SQL

        return _types[_type](value)

    except (ValueError, AttributeError, decimal.InvalidOperation):
        raise exceptions.ValueNotValid(value, field, _type)


def __record_asdict(fields: str, values: str) -> dict[str, str]:
    fields_list = fields.lower().replace(" ", "").split(",")
    values_list = values.replace(" ", "").split(",")

    return dict(zip(fields_list, values_list))

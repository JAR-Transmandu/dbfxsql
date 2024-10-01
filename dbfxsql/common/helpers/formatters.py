import decimal
from . import file_manager
from ..entities import constants, models, exceptions


def format_input(fields: str, values: str, types: list[str]) -> dict[str, any]:
    """Formats input data into a dictionary."""

    record: dict[str, any] = _record_asdict(fields, values)

    for field, value, _type in zip(record.keys(), record.values(), types):
        record[field] = _assign_type(field, value, _type)

    return record


def format_output(records: list[dict[str, any]]) -> list[dict[str, any]]:
    """Formats output data by converting fields to lowercase and stripping values."""

    lower_keys: list[str] = [key.lower() for key in records[0].keys()]

    for record in records:
        for key in record.keys():
            record[key] = (
                record[key].rstrip() if isinstance(record[key], str) else record[key]
            )

    return [dict(zip(lower_keys, record.values())) for record in records]


def parse_condition(condition: str) -> models.Filter:
    """Parses a condition string into a Filter object."""

    parameters: list[str] = condition.split(" ")

    if 2 < len(parameters):
        for parameter in parameters[3:]:
            parameters[2] += " " + parameter

    # operator
    if "=" == (parameters[1]):
        parameters[1] += "="

    # value
    if isinstance(parameters[2], str):
        parameters[2] = f"'{parameters[2]}'"

    return models.Filter(*parameters)


def filter_records(_records: list, filter: models.Filter, limit: int = -1) -> tuple:
    """Filters a list of records based on a given filter.

    Args:
        _records: The list of records to filter.
        filter: The filter to apply.
        limit: The maximum number of records to return.

    Returns:
        A tuple containing the filtered records and their corresponding indices.
    """

    records: list = []
    indexes: list = []
    count: int = 0

    for index, record in enumerate(_records):
        condition: str = filter.operator

        if isinstance(record[filter.field], str):
            condition = f"'{record[filter.field]}'{condition}{filter.value}"
        else:
            condition = f"{record[filter.field]}{condition}{filter.value.strip("'")}"

        if eval(condition):
            records.append(record)
            indexes.append(index)
            count -= -1  # count++

        if count == limit:
            break

    return records, indexes


def depurate_empty_records(records: list[dict]) -> list:
    """Return an empty list if a list of records only contains empty records."""

    if not records:
        return records

    if [{""}] == [{record for record in records.values()} for records in records]:
        return []

    return records


def parse_filepaths(changes: list[set]) -> list:
    """Retrieves the modified file from the environment variables."""

    filenames: list = []

    for change in changes:
        filepath: str = change[-1]
        name, extension = file_manager.decompose_filename(filepath)
        filenames.append(f"{name}.{extension}")

    return filenames


def package_fields(origin: models.Actor, destiny: models.Actor) -> tuple[str, str]:
    """Returns a tuple of fields to be compared."""

    return zip(origin.fields[0].split(", "), destiny.fields[0].split(", "))


def _record_asdict(fields: str, values: str) -> dict[str, str]:
    """Creates a dictionary from a list of fields and values."""

    fields_list = fields.lower().replace(" ", "").split(",")
    values_list = values.replace(" ", "").split(",")

    return dict(zip(fields_list, values_list))


def _assign_type(field, value: str, _type: str) -> any:
    """Assigns the appropriate type to a value based on its field and type."""

    try:
        # Logical case
        if "L" == _type and ("True" != value != "False"):
            raise exceptions.ValueNotValid(value, field, "bool")

        # Date/Datetime case
        if "D" == _type or "@" == _type:
            value.replace("/", "-")

        _types = constants.DBF if _type in constants.DBF.keys() else constants.SQL

        return _types[_type](value)

    except (ValueError, AttributeError, decimal.InvalidOperation):
        raise exceptions.ValueNotValid(value, field, _type)

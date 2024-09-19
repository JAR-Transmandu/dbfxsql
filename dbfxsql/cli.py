import click

from dbfxsql.functionalities import dbf_controller, sql_controller, sync_controller
from dbfxsql.common import models, utils


@click.group(cls=models.OrderCommands)
def cli():
    """This script helps with the initialization of the tool."""


@cli.command()
@click.option("-db", "--database", help="Name of the SQL database.")
@click.option("-t", "--table", help="Name of the DBF/SQL table.")
@click.option(
    "-f",
    "--field",
    type=(str, str),
    multiple=True,
    help="Field of the table with their DBF/SQL type.",
)
def create(database: str, table: str, field: tuple[tuple[str, str], ...]) -> None:
    """
    Create a new SQL database or a new DBF/SQL table.

    \b
    Examples:
    ----------
    - DBF TABLE => dbfxsql create -t users -f id N(20,0) -f name C(20)
    - SQL DB    => dbfxsql create -db users
    - SQL TABLE => dbfxsql create -db users -t users -f id "integer primary key" -f name text
    """
    # Errors
    if not (database or table):
        raise click.UsageError(
            "Missing option '-db' / '--database' or '-t' / '--table'."
        )
    if table and not field:
        raise click.UsageError("Missing option '-f' / '--field'.")
    if not table and field:
        raise click.UsageError("Missing option '-t' / '--table'.")

    # Use cases
    if database and table:
        fields = ", ".join([f"{field[0]} {field[1]}" for field in field])
        sql_controller.create_table(database, table, fields)
    elif table:
        fields = "; ".join([f"{field[0]} {field[1]}" for field in field])
        dbf_controller.create_table(table, fields)
    elif database:
        sql_controller.create_database(database)
    else:
        raise click.UsageError("Unknown behavior.")


@cli.command()
@click.option("-db", "--database", help="Name of the SQL database.")
@click.option("-t", "--table", help="Name of the DBF/SQL table.")
@click.confirmation_option(
    prompt="Are you sure you want to drop?", help="Confirm the operation."
)
def drop(database: str, table: str):
    """
    Drop an existing SQL database or an existing DBF/SQL table.

    \b
    Examples:
    ----------
    - DBF TABLE => dbfxsql drop -t users
    - SQL DB    => dbfxsql drop -db users
    - SQL TABLE => dbfxsql drop -db users -t users
    """
    # Errors
    if not (database or table):
        raise click.UsageError(
            "Missing option '-db' / '--database' or '-t' / '--table'."
        )

    # Use cases
    if database and table:
        sql_controller.drop_table(database, table)

    elif table:
        dbf_controller.drop_table(table)

    elif database:
        sql_controller.drop_database(database)

    else:
        raise click.UsageError("Unknown behavior.")


@cli.command()
@click.option("-t", "--table", required=True, help="Name of the DBF/SQL table.")
@click.option(
    "-f",
    "--field",
    required=True,
    type=(str, str),
    multiple=True,
    help="Field of the table with their DBF/SQL type.",
)
@click.option("--increment", is_flag=True, help="Set an increment int in id field.")
def add(table: str, field: tuple[tuple[str, str], ...], increment: bool):
    """
    Add fields with their DBF types to an existing table.

    \b
    Examples:
    ----------
    - DBF TABLE => dbfxsql add -t users -f id "N(20,0)" -f name "C(20)" --increment
    """
    # Handle input
    fields = "; ".join([f"{field[0]} {field[1]}" for field in field])

    # Use case
    dbf_controller.add_fields(table, fields, str(increment))


@cli.command()
@click.option("-db", "--database", help="Name of the SQL database.")
@click.option("-t", "--table", required=True, help="Name of the DBF/SQL table.")
@click.option(
    "-f",
    "--field",
    type=(str, str),
    multiple=True,
    required=True,
    help="Field and value pair as data to be inserted.",
)
def insert(
    database: str | None,
    table: str,
    field: tuple[tuple[str, str], ...],
):
    """
    Insert a new record to an existing DBF/SQL table.

    \b
    Examples:
    ----------
    - DBF TABLE => dbfxsql insert -t users -f id 1 -f name John
    - SQL TABLE => dbfxsql insert -db users -t users -f id 1 -f name John
    """
    # Handle input
    fields = ", ".join(f"{f[0]}" for f in field)
    values = ", ".join(f"{f[1]}" for f in field)

    if not database:
        dbf_controller.insert_record(table, fields, values)
    else:
        sql_controller.insert_record(database, table, fields, values)


@cli.command()
@click.option("-db", "--database", help="Name of the SQL database.")
@click.option("-t", "--table", required=True, help="Name of the DBF/SQL table.")
@click.option(
    "-c",
    "--condition",
    type=(str, str, str),
    help="Field, operator and value to filter records.",
)
def read(database: str | None, table: str, condition: tuple[str, str, str] | None):
    """
    Read existing records from an existing DBF/SQL table.

    \b
    Examples:
    ----------
    - DBF TABLE => dbfxsql read -t users -c id == 1
    - SQL TABLE => dbfxsql read -db users -t users -c id == 1
    """
    condition = f"{condition[0]} {condition[1]} {condition[2]}" if condition else None

    # Use cases
    if not database:
        utils.show_table(dbf_controller.read_records(table, condition))
    else:
        sql_controller.read_records(database, table, condition)
        # utils.show_table(sql_controller.read_records(database, table, condition))


@cli.command()
@click.option("-db", "--database", help="Name of the SQL database.")
@click.option("-t", "--table", required=True, help="Name of the DBF/SQL table.")
@click.option(
    "-f",
    "--field",
    type=(str, str),
    multiple=True,
    required=True,
    help="Field and value pair as data to be updated.",
)
@click.option(
    "-c",
    "--condition",
    type=(str, str, str),
    required=True,
    help="Field, operator and value to filter records.",
)
def update(
    database: str | None,
    table: str,
    field: tuple[tuple[str, str], ...],
    condition: tuple[str, str, str],
):
    """
    Update existing records from an existing DBF/SQL table.

    \b
    Examples:
    ----------
    - DBF TABLE => dbfxsql update -t users -f id 1 -f name John -c id == 1
    - SQL TABLE => dbfxsql update -db users -t users -f id 1 -f name John -c id == 1
    """

    # Handle input
    fields = ", ".join(f"{f[0]}" for f in field)
    values = ", ".join(f"{f[1]}" for f in field)
    condition = f"{condition[0]} {condition[1]} {condition[2]}" if condition else None

    # Use cases
    if not database:
        dbf_controller.update_records(table, fields, values, condition)
    else:
        sql_controller.update_records(database, table, fields, values, condition)


@cli.command()
@click.option("-db", "--database", help="Name of the SQL database.")
@click.option("-t", "--table", required=True, help="Name of the DBF/SQL table.")
@click.option(
    "-c",
    "--condition",
    type=(str, str, str),
    required=True,
    help="Field, operator and value to filter records.",
)
def delete(database: str | None, table: str, condition: tuple[str, str, str]):
    """
    Delete existing records from an existing DBF/SQL table.

    \b
    Examples:
    ----------
    - DBF TABLE => dbfxsql delete -t users -c id == 1
    - SQL TABLE => dbfxsql delete -db users -t users -c id == 1
    """
    condition = f"{condition[0]} {condition[1]} {condition[2]}" if condition else None

    # Use cases
    if not database:
        dbf_controller.delete_records(table, condition)
    else:
        sql_controller.delete_records(database, table, condition)


@cli.command()
def sync():
    """
    Synchronize data between DBF and SQL databases.
    """
    sync_controller.main()

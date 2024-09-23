"""Initialization module for the application"""

import click
from dbfxsql.common import models


@click.group(
    cls=models.LazyGroup,
    import_name="dbfxsql.cli:cli",
    epilog="For more information, visit https://github.com/j4breu/dbfxsql",
)
def run():
    """
    DBFxSQL is a CLI tool to manage data between DBF and SQL databases.

    You need to set the folders where DBF and SQL databases are located to work.
    """

"""Initialization module for the application"""

import click
from dbfxsql.common import models


@click.group(
    cls=models.LazyGroup,
    import_name="dbfxsql.cli:cli",
    epilog="For more information, visit https://github.com/j4breu/dbfxsql",
)
def run():
    """A CLI tool to manage data between DBF files and SQL databases."""

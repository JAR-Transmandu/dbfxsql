"""Auxiliary tasks of the application"""

from pathlib import Path

DBF_DATABASE = Path.cwd() / "dbf2sql_sync" / "common" / "databases" / "users.dbf"
SQL_DATABASE = Path.cwd() / "dbf2sql_sync" / "common" / "databases" / "users.sql"


def reset_databases() -> None:
    """Delete the database and storage to create them again"""

    if DBF_DATABASE.exists() or SQL_DATABASE.exists():
        SQL_DATABASE.unlink()
        DBF_DATABASE.unlink()

    DBF_DATABASE.touch()
    SQL_DATABASE.touch()

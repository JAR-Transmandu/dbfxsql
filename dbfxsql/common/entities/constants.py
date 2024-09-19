import datetime
import decimal
from pathlib import Path
from decouple import config

POOL: Path = Path(config("STORAGE_FOLDERPATH")) / "pool.json"

DBF: dict[str, any] = {
    "C": str,
    "D": datetime.date,
    "N": decimal.Decimal,
    "L": bool,
    "M": str,
    "F": float,
    "@": datetime.datetime,
}

SQL: dict[str, any] = {
    "NULL": None,
    "INTEGER": int,
    "REAL": float,
    "TEXT": str,
    "BLOB": bytes,
}

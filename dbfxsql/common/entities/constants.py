import datetime
import decimal


DBF: dict[str, any] = {
    "C": str,
    "D": datetime.date,
    "N": decimal.Decimal,  # Numeric
    "L": bool,
    "M": str,  # Memo (long text)
    "F": float,
    "@": datetime.datetime,
}

SQL: dict[str, any] = {
    "NULL": None,
    "INTEGER": int,
    "REAL": float,
    "TEXT": str,
    "BLOB": bytes,  # Binary data
}

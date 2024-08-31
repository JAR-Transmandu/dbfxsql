from dataclasses import dataclass
from typing import Any


@dataclass
class Data:
    table: str
    headers: str | None = None
    values: str | None = None
    condition: str | None = None


@dataclass
class Result:
    values: dict[str, Any, ...] | None

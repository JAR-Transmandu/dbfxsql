import sys


class ErrorTemplate(Exception):
    """Base class for custom error messages."""

    def __init__(self, message: str):
        self.message = message
        sys.exit(self)

    def __str__(self) -> str:
        return f"Error: {self.message}"


class FileNotFound(ErrorTemplate):
    def __init__(self, filepath: str):
        super().__init__(f"File not found at '{filepath}'.")


class DatabaseAlreadyExists(ErrorTemplate):
    def __init__(self, db_name: str):
        super().__init__(f"Database '{db_name}' already exists.")


class DatabaseNotFound(ErrorTemplate):
    def __init__(self, filepath: str):
        super().__init__(f"Database not found at '{filepath}'.")


class TableAlreadyExists(ErrorTemplate):
    def __init__(self, table_name: str):
        super().__init__(f"Table '{table_name}' already exists.")


class TableNotFound(ErrorTemplate):
    def __init__(self, table_name: str):
        super().__init__(f"Table '{table_name}' not found.")


class RecordNotFound(ErrorTemplate):
    def __init__(self, condition: str):
        super().__init__(f"Record not found with: {condition}")


class RecordAlreadyExists(ErrorTemplate):
    def __init__(self, record_id: int):
        super().__init__(f"Record already exists with id: {record_id}")


class ValueNotValid(ErrorTemplate):
    """Error raised when a value is not valid for a given field and type."""

    def __init__(self, value: str, field: str, _type: str):
        super().__init__(
            f"Value '{value}' not valid for field '{field}' with type '{_type}'"
        )

"""Structures oriented to the transmission of custom errors"""

import sys


class ErrorTemplate(Exception):
    def __init__(self, msg):
        self.args = (f"Error: {msg}",)
        sys.exit(self)


class FileNotFound(ErrorTemplate):
    def __init__(self, filepath):
        super().__init__(f"File not found at '{filepath}'.")


class DatabaseAlreadyExists(ErrorTemplate):
    def __init__(self, db):
        super().__init__(f"Database '{db}' already exists.")


class DatabaseNotFound(ErrorTemplate):
    def __init__(self, filepath):
        super().__init__(f"Database not found at '{filepath}'.")


class TableAlreadyExists(ErrorTemplate):
    def __init__(self, table):
        super().__init__(f"Table '{table}' already exists.")


class TableNotFound(ErrorTemplate):
    def __init__(self, table):
        super().__init__(f"Table '{table}' not found.")


class RecordNotFound(ErrorTemplate):
    def __init__(self, condition):
        super().__init__(f"Record not found with: {condition}")


class RecordAlreadyExists(ErrorTemplate):
    def __init__(self, id):
        super().__init__(f"Record already exists with id: {id}")


class ValueNotValid(ErrorTemplate):
    def __init__(self, value, field, _type):
        super().__init__(
            f"Value '{value}' not valid for field '{field}' with type '{_type}'"
        )

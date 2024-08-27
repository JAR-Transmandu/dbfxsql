from .. import dbf_controller
from .. import sql_controller


def dbf_to_sql() -> None:
    for record in dbf_controller.list_records():
        sql_controller.insert_record(record)


def sql_to_dbf() -> None:
    for record in sql_controller.list_records():
        dbf_controller.insert_record(record)

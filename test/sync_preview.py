from dbf2sql_sync.common import utils
from dbf2sql_sync.functionalities import sync_controller, dbf_controller, sql_controller


def test_dbf_to_sql(fields: str) -> None:
    print("\nRunning DBF -> SQL tests...", end="\n\n")
    sql_controller.reset_tables(fields)

    print("DROP TABLE users;", end="\n")
    print(f"CREATE TABLE users ({fields});")
    utils.show_table(sql_controller.list_records())

    print("Syncing...")
    utils.show_table(dbf_controller.list_records())
    sync_controller.dbf_to_sql()
    utils.show_table(sql_controller.list_records())

    print("DBF -> SQL test done!")


def test_sql_to_dbf(fields: str) -> None:
    print("\nRunning SQL -> DBF tests...", end="\n\n")
    dbf_controller.reset_tables(fields)

    print("DROP TABLE users;", end="\n")
    print(f"CREATE TABLE users ({fields});")
    utils.show_table(dbf_controller.list_records())

    print("Syncing...")
    utils.show_table(sql_controller.list_records())
    sync_controller.sql_to_dbf()
    utils.show_table(dbf_controller.list_records())

    print("SQL -> DBF test done!")


if __name__ == "__main__":
    test_dbf_to_sql("id int, name text, password text")
    test_sql_to_dbf("id N(20,0); name C(20); password C(20)")

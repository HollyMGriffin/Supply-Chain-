import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "supply_chain.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def orders_table_needs_in_transit(connection):
    row = connection.execute(
        "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'orders'"
    ).fetchone()

    return row is not None and "In Transit" not in row["sql"]


def initialize_database():
    connection = get_connection()

    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            schema = file.read()

        # Older databases were created before the 'In Transit' status
        # existed. SQLite can't change a CHECK constraint in place, so
        # rebuild the orders table and copy the existing rows across.
        if orders_table_needs_in_transit(connection):
            connection.executescript(
                "BEGIN;"
                "ALTER TABLE orders RENAME TO orders_old;"
                + schema +
                "INSERT INTO orders SELECT * FROM orders_old;"
                "DROP TABLE orders_old;"
                "COMMIT;"
            )
        else:
            connection.executescript(schema)

        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()

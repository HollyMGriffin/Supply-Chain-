
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "inventory.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = get_connection()

    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            connection.executescript(file.read())

        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()

import sqlite3
from pathlib import Path

from passwords import hash_password

BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "supply_chain.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

# The starting admin account, created only when the database has no
# accounts at all, such as the first time the app runs. Existing
# accounts are never changed. Log in with these and change the
# password straight away.
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "ChangeMe123"

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def create_default_admin(connection):
    account = connection.execute("SELECT id FROM users LIMIT 1").fetchone()

    if account is None:
        connection.execute(
            """
            INSERT INTO users (username, password_hash, display_name, role)
            VALUES (?, ?, 'Admin', 'Admin')
            """,
            (DEFAULT_ADMIN_USERNAME, hash_password(DEFAULT_ADMIN_PASSWORD))
        )


def initialize_database():
    connection = get_connection()

    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            connection.executescript(file.read())

        create_default_admin(connection)

        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()

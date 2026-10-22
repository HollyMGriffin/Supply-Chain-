
from database import get_connection


def get_user_by_username(username):
    connection = get_connection()
    try:
        row = connection.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        connection.close()

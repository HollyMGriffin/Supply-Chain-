
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


def get_user_by_id(user_id):
    connection = get_connection()
    try:
        row = connection.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        connection.close()


def get_all_users():
    """
    Returns every account without its password hash.
    """
    connection = get_connection()
    try:
        rows = connection.execute(
            "SELECT id, username, display_name, role FROM users ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def add_user(username, password_hash, display_name, role):
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            INSERT INTO users (username, password_hash, display_name, role)
            VALUES (?, ?, ?, ?)
            """,
            (username, password_hash, display_name, role)
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def update_password(user_id, password_hash):
    connection = get_connection()
    try:
        cursor = connection.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (password_hash, user_id)
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()

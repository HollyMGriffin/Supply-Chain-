from database import get_connection


def get_all_orders():
    connection = get_connection()

    try:
        rows = connection.execute(
            "SELECT * FROM orders ORDER BY id DESC"
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()

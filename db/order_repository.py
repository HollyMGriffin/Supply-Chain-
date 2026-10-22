
from database import get_connection


def get_all_orders(statuses=None):
    """
    Returns all orders, or only the ones whose status is in statuses.
    """
    connection = get_connection()
    try:
        if statuses is None:
            rows = connection.execute(
                "SELECT * FROM orders ORDER BY id DESC"
            ).fetchall()
        else:
            placeholders = ", ".join("?" for _ in statuses)
            rows = connection.execute(
                f"SELECT * FROM orders WHERE status IN ({placeholders}) "
                "ORDER BY id DESC",
                tuple(statuses)
            ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def get_order(order_id):
    connection = get_connection()
    try:
        row = connection.execute(
            "SELECT * FROM orders WHERE id = ?", (order_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        connection.close()


def add_order(data):
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            INSERT INTO orders
            (material, quantity, supplier, cost_cents,
             expected_arrival, required_by_date, status)
            VALUES (?, ?, ?, ?, ?, ?, 'Pending')
            """,
            (
                data["material"],
                data["quantity"],
                data["supplier"],
                data["cost_cents"],
                data["expected_arrival"],
                data["required_by_date"]
            )
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def update_order(order_id, data):
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            UPDATE orders
            SET material = ?, quantity = ?, supplier = ?,
                expected_arrival = ?, required_by_date = ?
            WHERE id = ? AND status = 'Pending'
            """,
            (
                data["material"],
                data["quantity"],
                data["supplier"],
                data["expected_arrival"],
                data["required_by_date"],
                order_id
            )
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def cancel_order(order_id):
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            UPDATE orders
            SET status = 'Canceled'
            WHERE id = ? AND status = 'Pending'
            """,
            (order_id,)
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()

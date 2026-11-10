
from database import get_connection


def get_all_orders(statuses=None):
    connection = get_connection()

    try:
        if statuses is None:
            rows = connection.execute(
                "SELECT * FROM orders ORDER BY id DESC"
            ).fetchall()
        else:
            if not statuses:
                return []

            placeholders = ", ".join("?" for _ in statuses)

            rows = connection.execute(
                f"""
                SELECT * FROM orders
                WHERE status IN ({placeholders})
                ORDER BY id DESC
                """,
                tuple(statuses)
            ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def get_order(order_id):
    connection = get_connection()

    try:
        row = connection.execute(
            "SELECT * FROM orders WHERE id = ?",
            (order_id,)
        ).fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


def add_order(data):
    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        inventory_id = data["inventory_id"]
        quantity = data["quantity"]

        stock = connection.execute(
            """
            SELECT material, quantity, cost_cents, location
            FROM inventory
            WHERE id = ?
            """,
            (inventory_id,)
        ).fetchone()

        if stock is None:
            raise ValueError("Selected inventory item does not exist.")

        if stock["quantity"] < quantity:
            raise ValueError(
                f"Only {stock['quantity']} units are available."
            )

        connection.execute(
            """
            UPDATE inventory
            SET quantity = quantity - ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (quantity, inventory_id)
        )

        cursor = connection.execute(
            """
            INSERT INTO orders (
                inventory_id,
                material,
                quantity,
                supplier,
                cost_cents,
                expected_arrival,
                required_by_date,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending')
            """,
            (
                inventory_id,
                stock["material"],
                quantity,
                stock["location"],
                stock["cost_cents"] * quantity,
                data["expected_arrival"],
                data["required_by_date"]
            )
        )

        connection.commit()
        return cursor.lastrowid

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def update_order(order_id, data):
    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        old = connection.execute(
            """
            SELECT *
            FROM orders
            WHERE id = ? AND status = 'Pending'
            """,
            (order_id,)
        ).fetchone()

        if old is None:
            return False

        new_id = data["inventory_id"]
        new_quantity = data["quantity"]

        stock = connection.execute(
            """
            SELECT material, quantity, cost_cents, location
            FROM inventory
            WHERE id = ?
            """,
            (new_id,)
        ).fetchone()

        if stock is None:
            raise ValueError("Selected inventory item does not exist.")

        available = stock["quantity"]

        if new_id == old["inventory_id"]:
            available += old["quantity"]

        if available < new_quantity:
            raise ValueError(
                f"Only {available} units are available."
            )

        connection.execute(
            """
            UPDATE inventory
            SET quantity = quantity + ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (old["quantity"], old["inventory_id"])
        )

        connection.execute(
            """
            UPDATE inventory
            SET quantity = quantity - ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (new_quantity, new_id)
        )

        cursor = connection.execute(
            """
            UPDATE orders
            SET inventory_id = ?,
                material = ?,
                quantity = ?,
                supplier = ?,
                cost_cents = ?,
                expected_arrival = ?,
                required_by_date = ?
            WHERE id = ? AND status = 'Pending'
            """,
            (
                new_id,
                stock["material"],
                new_quantity,
                stock["location"],
                stock["cost_cents"] * new_quantity,
                data["expected_arrival"],
                data["required_by_date"],
                order_id
            )
        )

        connection.commit()
        return cursor.rowcount > 0

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def cancel_order(order_id):
    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        order = connection.execute(
            """
            SELECT inventory_id, quantity
            FROM orders
            WHERE id = ? AND status = 'Pending'
            """,
            (order_id,)
        ).fetchone()

        if order is None:
            return False

        connection.execute(
            """
            UPDATE inventory
            SET quantity = quantity + ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (order["quantity"], order["inventory_id"])
        )

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

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


from datetime import date, timedelta

from database import get_connection


# Only orders in these statuses have not shipped yet, so their
# estimated arrival moves forward one day for each day that passes.
# In Transit, Delivered and Canceled orders keep their dates.
ROLLING_STATUSES = ("Pending", "Requested")


def roll_forward_arrivals(connection, today=None):
    """Move each unshipped order's expected arrival forward by the
    number of days since it was last moved, then remember today."""
    today = today or date.today()

    placeholders = ", ".join("?" for _ in ROLLING_STATUSES)

    rows = connection.execute(
        f"""
        SELECT id, expected_arrival, arrival_rolled_on, created_at
        FROM orders
        WHERE status IN ({placeholders})
          AND (arrival_rolled_on IS NULL OR arrival_rolled_on < ?)
        """,
        (*ROLLING_STATUSES, today.isoformat())
    ).fetchall()

    for row in rows:
        try:
            arrival = date.fromisoformat(row["expected_arrival"])
        except (TypeError, ValueError):
            continue

        if row["arrival_rolled_on"] is None:
            # Orders saved before this feature start counting today,
            # so their dates are not jumped forward all at once.
            days = 0
        else:
            days = (today - date.fromisoformat(row["arrival_rolled_on"])).days

        connection.execute(
            """
            UPDATE orders
            SET expected_arrival = ?,
                arrival_rolled_on = ?
            WHERE id = ?
            """,
            (
                (arrival + timedelta(days=max(days, 0))).isoformat(),
                today.isoformat(),
                row["id"]
            )
        )

    if rows:
        connection.commit()


def get_all_orders(statuses=None):
    connection = get_connection()

    try:
        roll_forward_arrivals(connection)

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
        roll_forward_arrivals(connection)

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
                status,
                arrival_rolled_on
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending', ?)
            """,
            (
                inventory_id,
                stock["material"],
                quantity,
                stock["location"],
                stock["cost_cents"] * quantity,
                data["expected_arrival"],
                data["required_by_date"],
                date.today().isoformat()
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
                required_by_date = ?,
                arrival_rolled_on = ?
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
                date.today().isoformat(),
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


def change_status(order_id, from_status, to_status):
    """Moves an order from one status to the next. Returns False if the
    order is no longer in from_status."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            "UPDATE orders SET status = ? WHERE id = ? AND status = ?",
            (to_status, order_id, from_status)
        )

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()


def request_order(order_id):
    return change_status(order_id, "Pending", "Requested")


def ship_order(order_id):
    return change_status(order_id, "Requested", "In Transit")


def count_orders_with_status(status):
    connection = get_connection()

    try:
        return connection.execute(
            "SELECT COUNT(*) FROM orders WHERE status = ?",
            (status,)
        ).fetchone()[0]

    finally:
        connection.close()


# How many days before the required-by (project start) date an order's
# estimated arrival starts to warn the Supply Chain Manager.
ARRIVAL_WARNING_DAYS = 3

# Orders that are still on their way and can still be acted on.
WARNING_STATUSES = ("Pending", "Requested", "In Transit")


def get_arrival_warnings(warning_days=ARRIVAL_WARNING_DAYS):
    """Orders whose estimated arrival is within warning_days of their
    required-by date, or after it, soonest required-by date first."""
    connection = get_connection()

    try:
        roll_forward_arrivals(connection)

        placeholders = ", ".join("?" for _ in WARNING_STATUSES)

        rows = connection.execute(
            f"""
            SELECT id, material, status, expected_arrival, required_by_date
            FROM orders
            WHERE status IN ({placeholders})
              AND date(expected_arrival) >= date(required_by_date, ?)
            ORDER BY required_by_date, id
            """,
            (*WARNING_STATUSES, f"-{int(warning_days)} days")
        ).fetchall()

        return [
            {**dict(row), "late": row["expected_arrival"] > row["required_by_date"]}
            for row in rows
        ]

    finally:
        connection.close()

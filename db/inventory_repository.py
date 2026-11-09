
from database import get_connection


# Get all inventory items
def get_all_inventory():
    connection = get_connection()

    try:
        rows = connection.execute(
            "SELECT * FROM inventory ORDER BY id DESC"
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


# Get one inventory item
def get_inventory_item(item_id):
    connection = get_connection()

    try:
        row = connection.execute(
            "SELECT * FROM inventory WHERE id = ?",
            (item_id,)
        ).fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


# Add inventory manually
def add_inventory(data):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO inventory (material, quantity, location, cost_cents)
            VALUES (?, ?, ?, ?)
            """,
            (
                data["material"],
                data["quantity"],
                data["location"],
                data["cost_cents"]
            )
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


# Edit an inventory item
def update_inventory(item_id, data):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE inventory
            SET material = ?,
                quantity = ?,
                location = ?,
                cost_cents = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                data["material"],
                data["quantity"],
                data["location"],
                data["cost_cents"],
                item_id
            )
        )

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()


# Delete an inventory item
def delete_inventory(item_id):
    connection = get_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM inventory WHERE id = ?",
            (item_id,)
        )

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()

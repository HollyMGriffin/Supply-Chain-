from datetime import date, timedelta

import database
from db.order_repository import get_arrival_warnings, roll_forward_arrivals


def days_from_today(days):
    return (date.today() + timedelta(days=days)).isoformat()


# ---- Login and permissions ----

def test_database_creates_default_admin(client):
    response = client.post(
        "/api/login",
        json={
            "username": database.DEFAULT_ADMIN_USERNAME,
            "password": database.DEFAULT_ADMIN_PASSWORD,
        },
    )
    assert response.status_code == 200
    assert response.get_json()["role"] == "Admin"


def test_login_page_loads_with_security_headers(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]


def test_wrong_password_is_rejected(client):
    response = client.post(
        "/api/login", json={"username": "admin", "password": "nope"}
    )
    assert response.status_code == 401


def test_pages_and_api_need_login(client):
    assert client.get("/orders").status_code == 302
    assert client.get("/api/orders").status_code == 401


def test_employee_cannot_add_orders_or_view_inventory(make_user, login_as):
    client = login_as(make_user("emp", "Employee"))
    assert client.post("/api/orders", json={}).status_code == 403
    assert client.get("/api/inventory").status_code == 403


# ---- Inventory and orders ----

def add_inventory(client, quantity):
    response = client.post(
        "/api/inventory",
        json={"material": "Steel Beams", "location": "Dock A",
              "quantity": quantity, "cost": "12.50"},
    )
    assert response.status_code == 201
    return response.get_json()["id"]


def test_inventory_rejects_html(make_user, login_as):
    client = login_as(make_user("wm", "Warehouse Manager"))
    response = client.post(
        "/api/inventory",
        json={"material": "<b>Steel</b>", "location": "A1",
              "quantity": 5, "cost": "1.00"},
    )
    assert response.status_code == 400


def test_order_moves_pending_requested_in_transit(make_user, login_as):
    make_user("wm", "Warehouse Manager")
    make_user("scm", "Supply Chain Manager")

    client = login_as("wm")
    item_id = add_inventory(client, quantity=10)

    login_as("scm")
    response = client.post(
        "/api/orders",
        json={"inventory_id": item_id, "quantity": 4,
              "expected_arrival": days_from_today(5),
              "required_by_date": days_from_today(20)},
    )
    assert response.status_code == 201
    order_id = response.get_json()["id"]

    order = client.get(f"/api/orders/{order_id}").get_json()
    assert order["status"] == "Pending"
    assert order["cost_cents"] == 4 * 1250

    # Ordering takes the units out of warehouse stock.
    assert client.get(f"/api/inventory/{item_id}").get_json()["quantity"] == 6

    assert client.post(f"/api/orders/{order_id}/request").status_code == 200
    # Only the Warehouse Manager can ship.
    assert client.post(f"/api/orders/{order_id}/ship").status_code == 403

    login_as("wm")
    assert client.post(f"/api/orders/{order_id}/ship").status_code == 200
    assert client.get(f"/api/orders/{order_id}").get_json()["status"] == "In Transit"


def test_order_cannot_exceed_stock(make_user, login_as):
    make_user("wm", "Warehouse Manager")
    make_user("scm", "Supply Chain Manager")

    client = login_as("wm")
    item_id = add_inventory(client, quantity=2)

    login_as("scm")
    response = client.post(
        "/api/orders",
        json={"inventory_id": item_id, "quantity": 3,
              "expected_arrival": days_from_today(1),
              "required_by_date": days_from_today(1)},
    )
    assert response.status_code == 400


# ---- Arrival date notifications ----

def insert_order(connection, arrival, required, rolled_on):
    cursor = connection.execute(
        "INSERT INTO inventory (material, quantity, location) VALUES ('Pipe', 0, 'B2')"
    )
    connection.execute(
        """
        INSERT INTO orders (inventory_id, material, quantity, supplier,
                            cost_cents, expected_arrival, required_by_date,
                            status, arrival_rolled_on)
        VALUES (?, 'Pipe', 1, 'B2', 100, ?, ?, 'Pending', ?)
        """,
        (cursor.lastrowid, arrival, required, rolled_on),
    )
    connection.commit()


def test_warning_when_arrival_is_close_to_required_date(db_path):
    today = date.today().isoformat()
    connection = database.get_connection()
    try:
        # Arrives 2 days before it is needed: inside the 3-day window.
        insert_order(connection, days_from_today(8), days_from_today(10), today)
        # Arrives weeks before it is needed: no warning.
        insert_order(connection, days_from_today(1), days_from_today(30), today)
    finally:
        connection.close()

    warnings = get_arrival_warnings()
    assert len(warnings) == 1
    assert warnings[0]["late"] is False


def test_pending_arrival_rolls_forward_one_day_per_day(db_path):
    connection = database.get_connection()
    try:
        insert_order(connection, "2026-12-10", "2026-12-31",
                     rolled_on=days_from_today(-2))
        roll_forward_arrivals(connection)
        row = connection.execute("SELECT expected_arrival FROM orders").fetchone()
    finally:
        connection.close()

    assert row["expected_arrival"] == "2026-12-12"

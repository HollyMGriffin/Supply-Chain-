from database import get_connection, initialize_database

initialize_database()

orders = [
    ("Steel Beams", 450, "Steeler Metals", 525000, "2026-12-25", "2026-12-30", "Pending"),
    ("Copper Wiring", 1200, "CoopCooper", 360000, "2026-12-22", "2026-12-28", "Pending"),
    ("Pipes", 300, "Pipe Supply Co.", 150000, "2026-12-20", "2026-12-24", "Delivered"),
    ("Drywall", 200, "Wood Makers", 240000, "2026-12-02", "2026-12-08", "Pending"),
    ("Concrete", 100, "BuildItRight Org.", 85000, "2026-12-19", "2026-12-23", "Canceled")
]

connection = get_connection()

try:
    count = connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0]

    if count == 0:
        for order in orders:
            connection.execute(
                """
                INSERT INTO orders
                (material, quantity, supplier, cost_cents,
                 expected_arrival, required_by_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                order
            )

        connection.commit()
        print("Sample orders added successfully!")

    # View all saved orders
    print("\nCurrent Orders:")

    for order in connection.execute("SELECT * FROM orders"):
        print(dict(order))

finally:
    connection.close()


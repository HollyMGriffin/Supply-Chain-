from database import get_connection, initialize_database

initialize_database()

orders = [
    ("Steel Beams", 450, "Steeler Metals", 525000, "2026-10-25", "2026-10-30", "Pending"),
    ("Copper Wiring", 1200, "CoopCooper", 360000, "2026-10-22", "2026-10-28", "Pending"),
    ("Pipes", 300, "Pipe Supply Co.", 150000, "2026-10-20", "2026-10-24", "Delivered"),
    ("Drywall", 200, "Wood Makers", 240000, "2026-11-02", "2026-11-08", "Pending"),
    ("Concrete", 100, "BuildItRight Org.", 85000, "2026-10-19", "2026-10-23", "Canceled")
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


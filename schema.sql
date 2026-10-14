CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    material TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    supplier TEXT NOT NULL,
    cost_cents INTEGER NOT NULL
        CHECK (cost_cents >= 0),

    expected_arrival TEXT NOT NULL,
    required_by_date TEXT NOT NULL,

    status TEXT NOT NULL DEFAULT 'Pending'
        CHECK (
            status IN (
                'Pending',
                'Delivered',
                'Canceled'
            )
        ),

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

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
                'In Transit',
                'Delivered',
                'Canceled'
            )
        ),

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL UNIQUE,
    -- Plaintext for the prototype only. Hash before real use.
    password TEXT NOT NULL,
    display_name TEXT NOT NULL,

    role TEXT NOT NULL
        CHECK (
            role IN (
                'Supply Chain Manager',
                'Warehouse Manager',
                'Employee'
            )
        )
);

INSERT OR IGNORE INTO users (username, password, display_name, role)
VALUES
    ('manager', '1234', 'Manager', 'Supply Chain Manager'),
    ('warehouse', '1234', 'Warehouse', 'Warehouse Manager'),
    ('employee', '1234', 'Employee', 'Employee');

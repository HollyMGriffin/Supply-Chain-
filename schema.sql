CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    material TEXT NOT NULL,
    inventory_id INTEGER NOT NULL REFERENCES inventory(id),
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
    -- Salted PBKDF2-SHA256 hash, made by passwords.hash_password.
    password_hash TEXT NOT NULL,
    display_name TEXT NOT NULL,

    role TEXT NOT NULL
        CHECK (
            role IN (
                'Admin',
                'Supply Chain Manager',
                'Warehouse Manager',
                'Employee'
            )
        )
);


-- Sprint 3: Warehouse Inventory

CREATE TABLE IF NOT EXISTS inventory (
                                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                                         material TEXT NOT NULL,
                                         supplier TEXT NOT NULL DEFAULT '',
                                         quantity INTEGER NOT NULL CHECK (quantity >= 0),
                                         location TEXT NOT NULL,
                                         cost_cents INTEGER NOT NULL DEFAULT 0 CHECK (cost_cents >= 0),
                                         updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

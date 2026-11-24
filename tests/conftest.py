import tempfile
from pathlib import Path

import pytest

import database
import passwords

# app.py sets up the database as soon as it is imported, so point it at a
# throwaway file first. Tests never touch the real supply_chain.db.
database.DATABASE_PATH = Path(tempfile.mkdtemp()) / "import.db"

# The real hash is deliberately slow (600,000 rounds). Tests only need it
# to work, not to be slow.
passwords.ITERATIONS = 1_000

import app as app_module  # noqa: E402
from db.user_repository import add_user  # noqa: E402

PASSWORD = "Password123"


@pytest.fixture
def db_path(tmp_path, monkeypatch):
    """A fresh, empty database for each test."""
    path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DATABASE_PATH", path)
    database.initialize_database()
    return path


@pytest.fixture
def client(db_path):
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as test_client:
        yield test_client


@pytest.fixture
def make_user(db_path):
    def _make(username, role):
        add_user(username, passwords.hash_password(PASSWORD), username, role)
        return username
    return _make


@pytest.fixture
def login_as(client):
    def _login(username):
        response = client.post(
            "/api/login", json={"username": username, "password": PASSWORD}
        )
        assert response.status_code == 200
        return client
    return _login

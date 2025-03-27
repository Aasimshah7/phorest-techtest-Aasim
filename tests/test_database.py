import pytest
import sqlite3
import os
from src.database import Database

@pytest.fixture
def db():
    db_path = "test_database.db"
    # Clean up before creating
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except PermissionError:
            try:
                conn = sqlite3.connect(db_path)
                conn.close()
                os.remove(db_path)
            except Exception:
                pass
    db = Database(db_path)
    yield db

def test_table_creation(db):
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        expected_tables = ["clients", "appointments", "services", "purchases"]
        assert all(table in tables for table in expected_tables)
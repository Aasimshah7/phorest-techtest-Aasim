import pytest
import sqlite3
import os
from src.database import Database
from src.data_loader import DataLoader

@pytest.fixture
def db():
    db_path = "test_data_loader.db"
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

def test_load_all_data(db):
    loader = DataLoader(db, "data")
    loader.load_all_data()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clients")
        assert cursor.fetchone()[0] > 0
        cursor.execute("SELECT COUNT(*) FROM appointments")
        assert cursor.fetchone()[0] > 0
        cursor.execute("SELECT COUNT(*) FROM services")
        assert cursor.fetchone()[0] > 0
        cursor.execute("SELECT COUNT(*) FROM purchases")
        assert cursor.fetchone()[0] > 0
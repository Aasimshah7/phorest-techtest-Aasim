import pytest
import sqlite3
import os
from src.database import Database
from src.data_loader import DataLoader
from src.loyalty import LoyaltyAnalyzer

@pytest.fixture
def db():
    db_path = "test_loyalty.db"
    
    # Ensure any existing database file is removed before creating a new one
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except PermissionError:
            # If we can't remove it immediately, close any potential connections
            try:
                conn = sqlite3.connect(db_path)
                conn.close()
                os.remove(db_path)
            except Exception:
                pass
    
    # Create and use the database
    db = Database(db_path)
    yield db

def test_get_top_clients(db):
    loader = DataLoader(db, "data")
    loader.load_all_data()
    
    analyzer = LoyaltyAnalyzer(db)
    top_clients = analyzer.get_top_clients(2, "2018-01-01")
    
    assert len(top_clients) <= 2
    assert all(client["points"] >= 0 for client in top_clients)
    assert all("first_name" in client and "last_name" in client and "email" in client 
               for client in top_clients)
from src.database import Database
from src.data_loader import DataLoader
from src.loyalty import LoyaltyAnalyzer

db = Database()
loader = DataLoader(db, "data")
loader.load_all_data()

analyzer = LoyaltyAnalyzer(db)
top_clients = analyzer.get_top_clients(50, "2018-01-01")  # From problem spec
for client in top_clients:
    print(f"{client['first_name']} {client['last_name']} ({client['email']}): {client['points']} points")
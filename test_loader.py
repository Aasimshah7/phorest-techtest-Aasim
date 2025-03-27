from src.database import Database
from src.data_loader import DataLoader

db = Database()
loader = DataLoader(db, "data")
loader.load_all_data()
print("Data loaded successfully!")
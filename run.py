import sys
from src.database import Database
from src.data_loader import DataLoader
from src.loyalty import LoyaltyAnalyzer

def main(top_n=50, since_date="2018-01-01"):
    db = Database()
    loader = DataLoader(db, "data")
    loader.load_all_data()

    analyzer = LoyaltyAnalyzer(db)
    top_clients = analyzer.get_top_clients(top_n, since_date)
    
    if not top_clients:
        print(f"No clients found with points since {since_date}.")
    else:
        print(f"Top {top_n} clients since {since_date}:")
        for i, client in enumerate(top_clients, 1):
            print(f"{i}. {client['first_name']} {client['last_name']} ({client['email']}): {client['points']} points")

if __name__ == "__main__":
    # Default values
    top_n = 50
    since_date = "2018-01-01"

    # Check command-line arguments
    if len(sys.argv) > 1:
        try:
            top_n = int(sys.argv[1])
            if len(sys.argv) > 2:
                since_date = sys.argv[2]
        except ValueError:
            print("Error: top_n must be an integer. Usage: python run.py [top_n] [since_date]")
            sys.exit(1)

    main(top_n, since_date)
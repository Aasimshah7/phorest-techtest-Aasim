import pandas as pd
from .database import Database

class DataLoader:
    def __init__(self, db: Database, data_dir: str):
        self.db = db
        self.data_dir = data_dir

    def load_all_data(self):
        conn = self.db.get_connection()
        try:
            clients_df = pd.read_csv(f"{self.data_dir}/clients.csv")
            clients_df.to_sql('clients', conn, if_exists='replace', index=False)
            
            appointments_df = pd.read_csv(f"{self.data_dir}/appointments.csv")
            appointments_df.to_sql('appointments', conn, if_exists='replace', index=False)
            
            services_df = pd.read_csv(f"{self.data_dir}/services.csv")
            services_df.to_sql('services', conn, if_exists='replace', index=False)
            
            purchases_df = pd.read_csv(f"{self.data_dir}/purchases.csv")
            purchases_df.to_sql('purchases', conn, if_exists='replace', index=False)
        finally:
            conn.close()  # Always close the connection
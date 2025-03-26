import sqlite3

class Database:
    def __init__(self, db_path="loyalty.db"):
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id TEXT PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT,
                    phone TEXT,
                    gender TEXT,
                    banned BOOLEAN
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    id TEXT PRIMARY KEY,
                    client_id TEXT,
                    start_time TEXT,
                    end_time TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS services (
                    id TEXT PRIMARY KEY,
                    appointment_id TEXT,
                    name TEXT,
                    price REAL,
                    loyalty_points INTEGER
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS purchases (
                    id TEXT PRIMARY KEY,
                    appointment_id TEXT,
                    name TEXT,
                    price REAL,
                    loyalty_points INTEGER
                )
            ''')
            conn.commit()

    def get_connection(self):
        return sqlite3.connect(self.db_path)
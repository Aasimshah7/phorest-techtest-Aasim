from .database import Database

class LoyaltyAnalyzer:
    def __init__(self, db: Database):
        self.db = db

    def get_top_clients(self, top_n: int, since_date: str):
        query = '''
            WITH LoyaltyPoints AS (
                SELECT 
                    c.id,
                    c.first_name,
                    c.last_name,
                    c.email,
                    c.banned,
                    COALESCE(SUM(s.loyalty_points), 0) + COALESCE(SUM(p.loyalty_points), 0) as total_points
                FROM clients c
                LEFT JOIN appointments a ON c.id = a.client_id
                LEFT JOIN services s ON a.id = s.appointment_id
                LEFT JOIN purchases p ON a.id = p.appointment_id
                WHERE a.start_time >= ? AND c.banned = 0
                GROUP BY c.id, c.first_name, c.last_name, c.email, c.banned
            )
            SELECT first_name, last_name, email, total_points
            FROM LoyaltyPoints
            ORDER BY total_points DESC
            LIMIT ?
        '''
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (since_date, top_n))
            return [{"first_name": row[0], "last_name": row[1], "email": row[2], "points": row[3]} 
                   for row in cursor.fetchall()]
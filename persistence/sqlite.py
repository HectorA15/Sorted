import sqlite3
from datetime import datetime

class FileHistoryDB:
    def __init__(self):
        self.db = sqlite3.connect('sorted_history.db')
        self.cursor = self.db.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS log (
                batch_id TEXT,
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_path TEXT,
                destination_path TEXT,
                timestamp DATETIME,
                rule_name TEXT
            )
        """)
        self.db.commit()
    
    def log_move(self, batch_id, source, destination, rule_name):
        sql = """
            INSERT INTO log(batch_id, source_path, destination_path, timestamp, rule_name)
            VALUES(?,?,?,?,?)
        """
        self.cursor.execute(sql, (batch_id, source, destination, datetime.now(), rule_name))
        self.db.commit()
    
    def get_all_moves(self):
        self.cursor.execute("""
            SELECT batch_id, id, source_path, destination_path, timestamp, rule_name
            FROM log
            ORDER BY timestamp DESC
        """)
        return self.cursor.fetchall()
    
    def get_last_move(self):
        self.cursor.execute("""
            SELECT * FROM log
            ORDER BY timestamp DESC 
            LIMIT 1;             
        """)
        result = self.cursor.fetchone()
        return result
    
    def delete_move(self, move_id):
        sql = "DELETE FROM log WHERE id = ?"
        self.cursor.execute(sql, (move_id,))
        self.db.commit()
    
    def close(self):
        self.db.close()
        pass
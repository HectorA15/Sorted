import sqlite3
from datetime import datetime
from pathlib import Path
from core.fs_utils import move_file
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
    
    def undo_batch(self):
        # Get the most recent batch_id
        self.cursor.execute("""
            SELECT batch_id FROM log
            GROUP BY batch_id
            ORDER BY MAX(timestamp) DESC
            LIMIT 1;
        """)
        result = self.cursor.fetchone()
        
        if not result:
            return {"reverted": [], "failed": [], "message": "No batch available to undo"}
        
        batch_id = result[0]
        
        # Now get all rows from that batch
        self.cursor.execute("""
            SELECT id, source_path, destination_path FROM log
            WHERE batch_id = ?
            ORDER BY id DESC
        """, (batch_id,))
        rows = self.cursor.fetchall()
        
        reverted = []
        failed = []
        
        for (_id, src, dst) in rows:
            try:
                if Path(dst).exists() and not Path(src).exists():
                    move_file(source=dst, dest_dir=Path(src).parent)
                    reverted.append((src, dst))
                elif not Path(dst).exists():
                    failed.append((src, dst, "Destination does not exist (possible rename/move/delete)"))
                elif Path(src).exists():
                    failed.append((src, dst, "Source already exists, will not overwrite"))
                else:
                    failed.append((src, dst, "Unexpected error"))
            except Exception as e:
                failed.append((src, dst, str(e)))
        
        # Delete the batch from history after reverting
        self.delete_batch(batch_id)
        
        return {"reverted": reverted, "failed": failed, "batch_id": batch_id}
    
    def delete_move(self, move_id):
        sql = "DELETE FROM log WHERE id = ?"
        self.cursor.execute(sql, (move_id,))
        self.db.commit()
    
    def delete_batch(self, batch_id):
        sql = "DELETE FROM log WHERE batch_id = ?"
        self.cursor.execute(sql, (batch_id,))
        self.db.commit()
    
    def close(self):
        self.db.close()
        pass
import sqlite3
import os

def save_to_db(records, db_path="data/osint.db"):
    """
    Saves OSINT records to SQLite database
    """
    try:
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Create table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS osint_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                user TEXT,
                timestamp TEXT,
                text TEXT,
                url TEXT,
                sentiment REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert records
        inserted = 0
        for r in records:
            try:
                cur.execute("""
                    INSERT INTO osint_data (platform, user, timestamp, text, url, sentiment)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    r.get("platform", "unknown"),
                    r.get("user", "unknown"),
                    r.get("timestamp", ""),
                    r.get("text", ""),
                    r.get("url", ""),
                    r.get("sentiment", 0.0)
                ))
                inserted += 1
            except Exception as e:
                print(f"  Warning: Could not insert record: {str(e)}")
                continue
        
        # Commit and close
        conn.commit()
        conn.close()
        
        print(f"✓ Saved {inserted} records to database: {db_path}")
        return inserted
        
    except Exception as e:
        print(f"✗ Database Error: {str(e)}")
        return 0

def get_record_count(db_path="data/osint.db"):
    """
    Returns the total number of records in the database
    """
    try:
        if not os.path.exists(db_path):
            return 0
        
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM osint_data")
        count = cur.fetchone()[0]
        conn.close()
        return count
    except:
        return 0

def export_to_csv(db_path="data/osint.db", csv_path="data/osint_export.csv"):
    """
    Exports database to CSV file
    """
    try:
        import pandas as pd
        
        conn = sqlite3.connect(db_path)
        df = pd.read_sql("SELECT * FROM osint_data", conn)
        conn.close()
        
        df.to_csv(csv_path, index=False)
        print(f"✓ Exported {len(df)} records to {csv_path}")
        return True
    except Exception as e:
        print(f"✗ Export Error: {str(e)}")
        return False

# Test function
if __name__ == "__main__":
    test_records = [
        {
            "platform": "test",
            "user": "testuser",
            "timestamp": "2025-01-01",
            "text": "Test message",
            "url": "https://test.com",
            "sentiment": 0.5
        }
    ]
    save_to_db(test_records, "data/test.db")
    print(f"Total records: {get_record_count('data/test.db')}")
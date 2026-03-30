import sqlite3
import os

db_path = os.path.abspath("data/audit_leads.db")
print(f"Checking database at: {db_path}")

if not os.path.exists(db_path):
    print("Database not found.")
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables: {tables}")
        
        if tables:
            for table_name in [t[0] for t in tables]:
                cursor.execute(f"SELECT status, COUNT(*) FROM {table_name} GROUP BY status;")
                rows = cursor.fetchall()
                print(f"Counts for table '{table_name}':")
                if not rows:
                    print("  No data found in this table.")
                for row in rows:
                    print(f"  {row[0]}: {row[1]}")
        else:
            print("No tables found in the database.")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

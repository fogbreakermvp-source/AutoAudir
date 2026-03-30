import sqlite3
import os

db_path = "data/audit_leads.db"
if not os.path.exists(db_path):
    print("Database not found.")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM leads GROUP BY status;")
    rows = cursor.fetchall()
    print("Lead Status Counts:")
    for row in rows:
        print(f"  {row[0]}: {row[1]}")
    conn.close()

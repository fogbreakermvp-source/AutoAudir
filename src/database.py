import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path="data/audit_leads.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                website TEXT,
                phone TEXT,
                address TEXT,
                rating REAL,
                reviews INTEGER,
                niche TEXT,
                location TEXT,
                audit_score INTEGER,
                load_time REAL,
                missing_alt_count INTEGER,
                broken_link_count INTEGER,
                ssl_issue BOOLEAN,
                status TEXT DEFAULT 'pending',
                report_path TEXT,
                contacted_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def add_lead(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Check if lead already exists by website or name+address
        cursor.execute("SELECT id FROM leads WHERE website = ? OR (name = ? AND address = ?)", 
                       (data.get('website'), data.get('name'), data.get('address')))
        if cursor.fetchone():
            conn.close()
            return False
        
        cursor.execute('''
            INSERT INTO leads (name, website, phone, address, rating, reviews, niche, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data.get('name'), data.get('website'), data.get('phone'), data.get('address'), 
              data.get('rating'), data.get('reviews'), data.get('niche'), data.get('location')))
        conn.commit()
        conn.close()
        return True

    def update_lead(self, lead_id, **kwargs):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for key, value in kwargs.items():
            cursor.execute(f"UPDATE leads SET {key} = ? WHERE id = ?", (value, lead_id))
        conn.commit()
        conn.close()

    def get_pending_leads(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM leads WHERE status = 'pending'")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

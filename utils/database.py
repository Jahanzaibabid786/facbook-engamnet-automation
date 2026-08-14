import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

class Database:
    def __init__(self, db_path: str = "database/app.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_schema()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_schema(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id TEXT UNIQUE NOT NULL,
                profile_name TEXT NOT NULL,
                profile_path TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'CREATING',
                device_id TEXT,
                created_at TEXT NOT NULL,
                last_used TEXT,
                last_validated TEXT,
                total_sessions INTEGER DEFAULT 0,
                metadata TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                status TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                duration INTEGER,
                details TEXT,
                FOREIGN KEY (profile_id) REFERENCES profiles(profile_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id TEXT NOT NULL,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                status TEXT NOT NULL,
                activities_completed INTEGER DEFAULT 0,
                error_message TEXT,
                FOREIGN KEY (profile_id) REFERENCES profiles(profile_id)
            )
        """)

        conn.commit()
        conn.close()

    def insert_profile(self, profile_data: Dict[str, Any]) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO profiles (
                profile_id, profile_name, profile_path, status, device_id,
                created_at, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            profile_data['profile_id'],
            profile_data['profile_name'],
            profile_data['profile_path'],
            profile_data.get('status', 'CREATING'),
            profile_data.get('device_id'),
            profile_data['created_at'],
            json.dumps(profile_data.get('metadata', {}))
        ))

        profile_pk = cursor.lastrowid
        conn.commit()
        conn.close()

        return profile_pk

    def update_profile(self, profile_id: str, updates: Dict[str, Any]):
        conn = self.get_connection()
        cursor = conn.cursor()

        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [profile_id]

        cursor.execute(f"""
            UPDATE profiles SET {set_clause} WHERE profile_id = ?
        """, values)

        conn.commit()
        conn.close()

    def get_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM profiles WHERE profile_id = ?", (profile_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def get_all_profiles(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if status:
            cursor.execute("SELECT * FROM profiles WHERE status = ? ORDER BY created_at DESC", (status,))
        else:
            cursor.execute("SELECT * FROM profiles ORDER BY created_at DESC")

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def insert_activity(self, activity_data: Dict[str, Any]) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO activities (
                profile_id, activity_type, status, timestamp, duration, details
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            activity_data['profile_id'],
            activity_data['activity_type'],
            activity_data['status'],
            activity_data['timestamp'],
            activity_data.get('duration'),
            json.dumps(activity_data.get('details', {}))
        ))

        activity_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return activity_id

    def insert_session(self, session_data: Dict[str, Any]) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sessions (
                profile_id, started_at, status
            ) VALUES (?, ?, ?)
        """, (
            session_data['profile_id'],
            session_data['started_at'],
            session_data['status']
        ))

        session_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return session_id

    def update_session(self, session_id: int, updates: Dict[str, Any]):
        conn = self.get_connection()
        cursor = conn.cursor()

        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [session_id]

        cursor.execute(f"""
            UPDATE sessions SET {set_clause} WHERE id = ?
        """, values)

        conn.commit()
        conn.close()

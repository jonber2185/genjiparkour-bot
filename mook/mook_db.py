import os
from dotenv import load_dotenv
import sqlite3
import csv

load_dotenv()

db_path = os.getenv("SQLITE_DB_PATH")
conn = sqlite3.connect(db_path)

def main():
    init_table()

    # insert map
    with open("./mook/map_list.txt", "r", encoding="utf-8") as file:
        map_list = file.read().split("\n")
        for map in map_list:
            conn.execute("INSERT INTO maps (name) VALUES (?)", (map, ))

    insert_code()

    conn.commit()
    conn.close()


def init_table():
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        is_blocked INTEGER DEFAULT 0
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS maps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS codes (
        code TEXT PRIMARY KEY,
        map_name TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        creator TEXT NOT NULL,
        cp INTEGER,
        description TEXT,
        guide TEXT,
        FOREIGN KEY (map_name) REFERENCES maps (name) ON UPDATE CASCADE ON DELETE CASCADE
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS user_tiers (
        user_id INTEGER PRIMARY KEY,
        tier TEXT DEFAULT 'G',
        easy_count INTEGER DEFAULT 0,
        medium_count INTEGER DEFAULT 0,
        hard_count INTEGER DEFAULT 0,
        veryhard_count INTEGER DEFAULT 0,
        extreme_count INTEGER DEFAULT 0,
        hell_count INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS user_clears (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        code TEXT NOT NULL,
        clear_time REAL NOT NULL,
        UNIQUE(user_id, code),
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
        FOREIGN KEY (code) REFERENCES codes (code) ON DELETE CASCADE
    )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_codes_map ON codes (map_name);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_codes_diff ON codes (difficulty);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_codes_creator ON codes (creator);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_users_blocked ON users (is_blocked);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_clears_user_id ON user_clears (user_id);")

def insert_code():
    # code, map_name, difficulty, cp, description, guide, creator
    
    rows = []
    with open('./mook/code_list.csv', encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        sql = """
        INSERT INTO codes (code, map_name, difficulty, creator, cp, description, guide)
        VALUES (:code, :map_name, :difficulty, :creator, :cp, :description, :guide)
        """
        data = {
            "code": row["code"].upper(),
            "map_name": row["map_name"],
            "difficulty": row["difficulty"],
            "creator": row["creator"].upper(),
            "cp": int(row["cp"]) if row["cp"] else None,
            "description": row["description"] or None,
            "guide": row["guide"] or None,
        }
        conn.execute(sql, data)



main()

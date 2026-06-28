import os
import sqlite3
from dotenv import load_dotenv
import logging
logger = logging.getLogger(__name__)

load_dotenv()

class SQLiteHandler:
    def __init__(self):
        self.conn = None

    def connect(self):
        if self.conn is None:
            db_path = os.getenv("SQLITE_DB_PATH", "db/data.db")
            self.conn = sqlite3.connect(db_path)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON;")
            self._init_tables()
            logger.info("DB 연결 완료")

    def _init_tables(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                is_blocked INTEGER DEFAULT 0
            )
            """)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS maps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
            """)
            self.conn.execute("""
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
            self.conn.execute("""
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
            self.conn.execute("""
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
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_codes_map ON codes (map_name);")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_codes_diff ON codes (difficulty);")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_codes_creator ON codes (creator);")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_users_blocked ON users (is_blocked);")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_clears_user_id ON user_clears (user_id);")
        logger.info("테이블 초기화 완료")

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("DB 연결 종료")
            self.conn = None

db_handler = SQLiteHandler()
import logging
from typing import Any
from ..db_handler import db_handler

logger = logging.getLogger(__name__)


class BaseRepository:
    def __init__(self):
        self._db = db_handler

    def fetch(
        self,
        sql: str,
        params: tuple | dict | None = None,
        fetchone: bool = False,
    ) -> dict | list[dict] | None:
        cur = self._db.conn.execute(sql, params or ())
        if fetchone:
            row = cur.fetchone()
            return dict(row) if row else None
        return [dict(r) for r in cur.fetchall()]

    def execute(self, sql: str, params: tuple | dict | None = None) -> Any:
        try:
            with self._db.conn:
                return self._db.conn.execute(sql, params or ())
        except Exception:
            logger.info("Database error")
            raise
from sqlite3 import IntegrityError
from db.entities import ClearEntity
from .base_repository import BaseRepository


class ClearRepository(BaseRepository):

    ### SELECT ###
    def select(self, code: str) -> list[ClearEntity]:
        sql = """
        SELECT user_id, code, clear_time
        FROM user_clears
        WHERE code = ?
        ORDER BY clear_time ASC
        LIMIT 20
        """
        rows = self.fetch(sql, (code.upper(),))
        return [ClearEntity.model_validate(row) for row in rows]
    
    def select_user(self, user_id: int) -> list[ClearEntity]:
        sql = """
        SELECT uc.user_id, uc.code, uc.clear_time, c.difficulty
        FROM user_clears uc
        INNER JOIN codes c ON uc.code = c.code
        WHERE uc.user_id = ?
        """
        rows = self.fetch(sql, (user_id,))
        results = [ClearEntity.model_validate(row) for row in rows]
        results.sort(key=lambda r: r.difficulty.weight)
        return results

    def get_data(self, code: str, user_id: int) -> ClearEntity | None:
        row = self.fetch(
            "SELECT * FROM user_clears WHERE code = ? AND user_id = ?",
            (code.upper(), user_id),
            fetchone=True,
        )
        if not row: return None
        else: return ClearEntity.model_validate(row)

    ### INSERT ###
    def insert(self, clear: ClearEntity):
        sql = """
        INSERT INTO user_clears (user_id, code, clear_time)
        VALUES (:user_id, :code, :clear_time)
        """
        data = clear.model_dump(mode="json")
        try:
            self.execute(sql, data)
        except IntegrityError as e:
            if "FOREIGN KEY" not in str(e):
                raise
            self.execute("INSERT INTO users (user_id) VALUES (?)", (clear.user_id,))
            self.execute(sql, data)

    ### UPDATE ###
    def update(self, clear: ClearEntity):
        row = self.get_data(code=clear.code, user_id=clear.user_id)
        if row.clear_time < clear.clear_time: return
        self.execute(
            "UPDATE user_clears SET clear_time = ? WHERE user_id = ? AND code = ?",
            (clear.clear_time, clear.user_id, clear.code.upper()),
        )

    ### DELETE ###
    def delete(self, clear: ClearEntity):
        self.execute(
            "DELETE FROM user_clears WHERE user_id = ? AND code = ?",
            (clear.user_id, clear.code.upper()),
        )
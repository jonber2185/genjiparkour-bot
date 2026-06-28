from db.entities import CodeEntity
from .base_repository import BaseRepository


class CodeRepository(BaseRepository):

    ### SELECT ###
    def select_codes(self) -> list[dict]:
        return self.fetch("SELECT code, map_name, creator FROM codes")

    def select(
        self,
        user_id: int,
        map_name: str = None,
        difficulty: str = None,
        creator: str = None,
        code: str = None,
    ) -> list[CodeEntity]:
        sql = """
        SELECT
            c.code,
            c.map_name,
            c.difficulty,
            c.creator,
            c.cp,
            c.description,
            c.guide,
            u.clear_time
        FROM codes c
        LEFT JOIN user_clears u
            ON c.code = u.code
            AND u.user_id = ?
        WHERE 1 = 1
        """
        params = [user_id]

        filters = {
            "map_name":   map_name,
            "difficulty": difficulty,
            "code":       code.upper() if code else None,
        }
        for column, value in filters.items():
            if value is not None:
                sql += f" AND c.{column} = ?"
                params.append(value)
            
        if creator is not None:
            sql += " AND creator LIKE ?"
            params.append(f"%{creator.upper()}%")

        rows = self.fetch(sql, tuple(params))
        results = [CodeEntity.model_validate(row) for row in rows]
        results.sort(key=lambda r: (r.map_name, r.difficulty.weight))
        return results

    def find_code(self, code: str) -> CodeEntity | None:
        row = self.fetch("SELECT * FROM codes WHERE code = ?", (code,), fetchone=True)
        return CodeEntity.model_validate(row) if row else None

    ### INSERT ###
    def insert(self, code: CodeEntity):
        sql = """
        INSERT INTO codes (code, map_name, difficulty, creator, cp, description, guide)
        VALUES (:code, :map_name, :difficulty, :creator, :cp, :description, :guide)
        """
        self.execute(sql, code.model_dump(mode="json"))

    ### UPDATE ###
    def update(self, code: str, updates: dict):
        if not updates:
            return
        set_clause = ", ".join(f"{key} = ?" for key in updates)
        params = (*updates.values(), code)
        self.execute(f"UPDATE codes SET {set_clause} WHERE code = ?", params)

    ### DELETE ###
    def delete(self, code: str):
        self.execute("DELETE FROM codes WHERE code = ?", (code,))
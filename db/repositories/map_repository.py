from .base_repository import BaseRepository


class MapRepository(BaseRepository):

    ### SELECT ###
    def select(self) -> list[str]:
        rows = self.fetch("SELECT name FROM maps")
        return [row["name"] for row in rows]

    def exists(self, map_name: str) -> bool:
        row = self.fetch("SELECT 1 FROM maps WHERE name = ?", (map_name,), fetchone=True)
        return row is not None

    ### INSERT ###
    def insert(self, map_name: str):
        self.execute("INSERT INTO maps (name) VALUES (?)", (map_name,))

    ### UPDATE ###
    def update(self, map_name: str, new_map_name: str):
        self.execute("UPDATE maps SET name = ? WHERE name = ?", (new_map_name, map_name))

    ### DELETE ###
    def delete(self, map_name: str):
        self.execute("DELETE FROM maps WHERE name = ?", (map_name,))
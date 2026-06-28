from sqlite3 import IntegrityError
from db.repositories import map_repository
from errors import errors


class MapService:
    def __init__(self):
        self.repository = map_repository

    def get_maps(self) -> list[str]:
        return self.repository.select()

    def add_map(self, map_name: str):
        try:
            self.repository.insert(map_name)
        except IntegrityError:
            raise errors.DBError.DuplicateError(f"맵 '{map_name}'은(는) 이미 등록된 맵입니다.")

    def update_map(self, map_name: str, new_map_name: str):
        if not self.repository.exists(map_name):
            raise errors.DBError.DataValidationError(f"'{map_name}'은(는) 존재하지 않는 맵입니다.")
        self.repository.update(map_name, new_map_name)

    def delete_map(self, map_name: str):
        if not self.repository.exists(map_name):
            raise errors.DBError.DataValidationError(f"'{map_name}'은(는) 존재하지 않는 맵입니다.")
        self.repository.delete(map_name)
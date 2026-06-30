from sqlite3 import IntegrityError
from db.repositories import user_repository
from errors import errors


class AnonymousBlockedUserService:
    def __init__(self):
        self.repository = user_repository

    def get_list(self) -> list[int]:
        return [row["user_id"] for row in self.repository.find_blocked_users()]

    def is_blocked(self, user_id: int) -> bool:
        user_id = int(user_id)
        result = self.repository.find_user(user_id)
        if not result:
            self.repository.insert(user_id)
            return False
        return bool(result["is_blocked"])

    def block_user(self, user_id: int, is_blocked: bool):
        user_id = int(user_id)
        if self.is_blocked(user_id) and is_blocked: raise errors.DBError.DuplicateError("이미 차단된 유저입니다.")
        self.repository.update(user_id=user_id, is_blocked=is_blocked)
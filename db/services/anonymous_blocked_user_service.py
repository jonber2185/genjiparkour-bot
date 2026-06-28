from sqlite3 import IntegrityError
from db.repositories import user_repository


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
        try:
            self.repository.update(user_id=user_id, is_blocked=is_blocked)
        except IntegrityError as e:
            if "FOREIGN KEY" not in str(e):
                raise
            self.repository.insert(user_id)
            self.repository.update(user_id=user_id, is_blocked=is_blocked)
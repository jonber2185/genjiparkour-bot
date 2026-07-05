from sqlite3 import IntegrityError
from db.repositories import user_repository


class UserService:
    def __init__(self):
        self.repository = user_repository

    def get_all_users(self) -> list[int]:
        users = self.repository.select()
        return [user['user_id'] for user in users]

    def delete_users(self, user_ids: list[int]):
        self.repository.delete(user_ids)
from sqlite3 import IntegrityError
from db.repositories import user_repository


class UserService:
    def __init__(self):
        self.repository = user_repository

    def add_user(self, user_id: int):
        try:
            self.repository.insert(int(user_id))
        except IntegrityError:
            pass

    def delete_user(self, user_id: int):
        self.repository.delete(int(user_id))
from .base_repository import BaseRepository


class UserRepository(BaseRepository):

    ### SELECT ###
    def find_user(self, user_id: int) -> dict | None:
        return self.fetch(
            "SELECT is_blocked FROM users WHERE user_id = ?",
            (user_id,),
            fetchone=True,
        )

    def find_blocked_users(self) -> list[dict]:
        return self.fetch("SELECT user_id FROM users WHERE is_blocked = 1")

    ### INSERT ###
    def insert(self, user_id: int):
        self.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

    ### UPDATE ###
    def update(self, user_id: int, is_blocked: bool):
        self.execute(
            "UPDATE users SET is_blocked = ? WHERE user_id = ?",
            (int(is_blocked), user_id),
        )

    ### DELETE ###
    def delete(self, user_id: int):
        self.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
from db.entities import TierEntity
from .base_repository import BaseRepository

ALLOWED_COUNT_COLUMNS = frozenset({
    "easy_count",
    "medium_count",
    "hard_count",
    "veryhard_count",
    "extreme_count",
    "hell_count",
})

ALLOWED_TIERS = frozenset({"G", "헉!", "와;;", "어?", "오;", "흠..", "좁"})


class TierRepository(BaseRepository):

    ### SELECT ###
    def find_users_tier(self) -> list[TierEntity]:
        sql = """
        SELECT *
        FROM user_tiers
        ORDER BY
            hell_count DESC,
            extreme_count DESC,
            veryhard_count DESC,
            hard_count DESC,
            medium_count DESC,
            easy_count DESC
        LIMIT 10
        """
        return [TierEntity.model_validate(row) for row in self.fetch(sql)]

    def find_user(self, user_id: int) -> dict | None:
        return self.fetch(
            "SELECT * FROM user_tiers WHERE user_id = ?",
            (user_id,),
            fetchone=True,
        )

    ### INSERT ###
    def insert(self, user_id: int):
        self.execute("INSERT INTO user_tiers (user_id) VALUES (?)", (user_id,))

    ### UPDATE ###
    def update_count(self, user_id: int, count_column: str):
        if count_column not in ALLOWED_COUNT_COLUMNS:
            raise ValueError(f"올바르지 않은 컬럼명입니다: {count_column}")
        self.execute(
            f"UPDATE user_tiers SET {count_column} = {count_column} + 1 WHERE user_id = ?",
            (user_id,),
        )

    def update_count_dec(self, user_id: int, count_column: str):
        if count_column not in ALLOWED_COUNT_COLUMNS:
            raise ValueError(f"올바르지 않은 컬럼명입니다: {count_column}")
        self.execute(
            f"UPDATE user_tiers SET {count_column} = {count_column} - 1 WHERE user_id = ?",
            (user_id,),
        )

    def update_tier(self, user_id: int, tier: str):
        if tier not in ALLOWED_TIERS:
            raise ValueError(f"올바르지 않은 티어입니다: {tier}")
        self.execute(
            "UPDATE user_tiers SET tier = ? WHERE user_id = ?",
            (tier, user_id),
        )
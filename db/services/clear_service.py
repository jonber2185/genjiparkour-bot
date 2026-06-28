from sqlite3 import IntegrityError
from db.entities import ClearEntity, TierEntity
from db.repositories import clear_repository, tier_repository, code_repository, user_repository
from errors import errors

DIFFICULTY_TO_COLUMN: dict[str, str] = {
    "Easy":     "easy_count",
    "Medium":   "medium_count",
    "Hard":     "hard_count",
    "VeryHard": "veryhard_count",
    "Extreme":  "extreme_count",
    "Hell":     "hell_count",
}


class ClearService:
    def __init__(self):
        self.clear_repo = clear_repository
        self.tier_repo = tier_repository
        self.code_repo = code_repository
        self.user_repo = user_repository

    def get_users_tier(self) -> list[TierEntity]:
        return self.tier_repo.find_users_tier()

    def get_user_tier(self, user_id: int) -> TierEntity:
        user_id = int(user_id)
        user_data = self.tier_repo.find_user(user_id)
        if not user_data:
            try:
                self.tier_repo.insert(user_id)
            except IntegrityError as e:
                if "FOREIGN KEY" not in str(e):
                    raise
                self.user_repo.insert(user_id)
                self.tier_repo.insert(user_id)
            user_data = self.tier_repo.find_user(user_id)
        return TierEntity.model_validate(user_data)

    def get_clear_users(self, code: str) -> list[ClearEntity]:
        return self.clear_repo.select(code)
    
    def get_clear_user(self, code: str, user_id: int) -> ClearEntity | None:
        return self.clear_repo.get_data(code=code, user_id=user_id)
    
    def get_user_clears(self, user_id: int) -> list[ClearEntity]:
        return self.clear_repo.select_user(user_id=user_id)


    def clear_code(self, clear: ClearEntity) -> tuple[str, str]:
        code_info = self.code_repo.find_code(clear.code)
        if code_info is None:
            raise errors.DBError.DataValidationError("해당 코드는 존재하지 않습니다.")
        
        if code_info.difficulty in ("etc", "Practice"):
            if self.clear_repo.get_data(code=clear.code, user_id=clear.user_id) is not None:
                self.clear_repo.update(clear)
            else: self.clear_repo.insert(clear)
            return "etc", "etc"

        user_info = self.get_user_tier(clear.user_id)

        if self.clear_repo.get_data(code=clear.code, user_id=clear.user_id) is not None:
            self.clear_repo.update(clear)
            return user_info.tier, user_info.tier

        self.clear_repo.insert(clear)

        base_difficulty = code_info.difficulty.replace("+", "").replace("-", "")
        column_name = DIFFICULTY_TO_COLUMN.get(base_difficulty)
        if not column_name:
            raise ValueError(f"지원하지 않는 난이도 형식입니다: {code_info.difficulty}")

        self.tier_repo.update_count(clear.user_id, column_name)
        user_info = user_info.increment_count(column_name=column_name)

        new_tier = self._calculate_tier(user_info)
        if user_info.tier != new_tier:
            self.tier_repo.update_tier(user_id=clear.user_id, tier=new_tier)

        return user_info.tier, new_tier

    def cancel_clear(self, clear: ClearEntity) -> tuple[str, str]:
        code_info = self.code_repo.find_code(clear.code)
        if code_info is None:
            raise errors.DBError.DataValidationError("해당 코드는 존재하지 않습니다.")
        
        if code_info.difficulty in ("etc", "Practice"):
            self.clear_repo.delete(clear=clear)
            return "etc", "etc"

        user_info = self.get_user_tier(clear.user_id)
        self.clear_repo.delete(clear=clear)

        base_difficulty = code_info.difficulty.replace("+", "").replace("-", "")
        column_name = DIFFICULTY_TO_COLUMN.get(base_difficulty)
        if not column_name:
            raise ValueError(f"지원하지 않는 난이도 형식입니다: {code_info.difficulty}")

        self.tier_repo.update_count_dec(clear.user_id, column_name)
        user_info = user_info.decrement_count(column_name=column_name)

        new_tier = self._calculate_tier(user_info)
        if user_info.tier != new_tier:
            self.tier_repo.update_tier(user_id=clear.user_id, tier=new_tier)

        return user_info.tier, new_tier

    def _calculate_tier(self, tier: TierEntity) -> str:
        if tier.hell_count >= 3:     return "헉!"
        if tier.extreme_count >= 5:  return "와;;"
        if tier.veryhard_count >= 7: return "어?"
        if tier.hard_count >= 10:    return "오;"
        if tier.medium_count >= 10:  return "흠.."
        if tier.easy_count >= 10:    return "좁"
        return "G" 
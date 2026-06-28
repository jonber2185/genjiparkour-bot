from pydantic import BaseModel, ConfigDict

class TierEntity(BaseModel):
    user_id: int
    tier: str
    easy_count: int
    medium_count: int
    hard_count: int
    veryhard_count: int
    extreme_count: int
    hell_count: int

    model_config = ConfigDict(from_attributes=True)

    def increment_count(self, column_name: str):
        current_value = getattr(self, column_name, 0)
        return self.model_copy(update={column_name: current_value + 1})

    def decrement_count(self, column_name: str):
        current_value = getattr(self, column_name, 0)
        return self.model_copy(update={column_name: current_value - 1})
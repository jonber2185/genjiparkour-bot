from typing import Optional
from pydantic import BaseModel, ConfigDict
from ..enums import Difficulty

class ClearEntity(BaseModel):
    user_id: int
    code: str
    clear_time: float
    difficulty: Optional[Difficulty] = None

    model_config = ConfigDict(from_attributes=True)
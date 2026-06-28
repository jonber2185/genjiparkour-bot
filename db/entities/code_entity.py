from typing import Optional
from pydantic import BaseModel, ConfigDict
from ..enums import Difficulty

class CodeEntity(BaseModel):
    code: str
    map_name: str
    difficulty: Difficulty
    creator: str
    cp: Optional[int] = None
    description: Optional[str] = None
    guide: Optional[str] = None
    clear_time: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
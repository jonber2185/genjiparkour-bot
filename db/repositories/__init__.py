from .user_repository import UserRepository
from .code_repository import CodeRepository
from .map_repository import MapRepository
from .clear_repository import ClearRepository
from .tier_repository import TierRepository

user_repository = UserRepository()
code_repository = CodeRepository()
map_repository = MapRepository()
clear_repository = ClearRepository()
tier_repository = TierRepository()

__all__ = [
    "user_repository",
    "code_repository",
    "map_repository",
    "clear_repository",
    "tier_repository",
]
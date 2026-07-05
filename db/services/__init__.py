from .map_service import MapService
from .map_autocomplete_service import MapAutocompleteService
from .code_service import CodeService
from .code_autocomplete_service import CodeAutocompleteService
from .anonymous_blocked_user_service import AnonymousBlockedUserService
from .clear_service import ClearService
from .user_service import UserService

map_service = MapService()
map_autocomplete_service = MapAutocompleteService()
code_service = CodeService()
code_autocomplete_service = CodeAutocompleteService()
anonymous_blocked_user_service = AnonymousBlockedUserService()
clear_service = ClearService()
user_service = UserService()

__all__ = [
    "map_service",
    "map_autocomplete_service",
    "code_service",
    "code_autocomplete_service",
    "anonymous_blocked_user_service",
    "clear_service",
    "user_service",
]
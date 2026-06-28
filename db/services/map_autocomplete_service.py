from db.repositories import map_repository

class MapAutocompleteService:
    def __init__(self):
        self.repository = map_repository
        self.maps = []

    def load_memory(self):
        rows = self.repository.select()
        self.maps = rows

    def get_suggestions(self, current_input: str):
        if not current_input:
            return self.maps[:25]
        
        suggestions = []
        for map in self.maps:
            if current_input in map:
                suggestions.append(map)
            if len(suggestions) >= 25:
                break
                
        return suggestions
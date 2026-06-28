from db.repositories import code_repository


class CodeAutocompleteService:
    def __init__(self):
        self.repository = code_repository
        self.codes = [] 

    def load_memory(self):
        rows = self.repository.select_codes()
        self.codes = [
            {"code": row['code'], "map_name": row['map_name']}
            for row in rows
        ]
        self.creators = list({row['creator'] for row in rows})

    def get_code_suggestions(self, current_input: str) -> list[dict]:
        if not current_input:
            return self.codes[:25]
        
        current_input = current_input.upper()
        
        suggestions = []
        for code in self.codes:
            # print(code)
            if current_input in code['code']:
                suggestions.append(code)
            if len(suggestions) >= 25:
                break
                
        return suggestions

    def get_creators_suggestions(self, current_input: str) -> list[str]:
        if not current_input:
            return self.creators[:25]
        
        current_input = current_input.upper()
        
        suggestions = []
        for creator in self.creators:
            if current_input in creator:
                suggestions.append(creator)
            if len(suggestions) >= 25:
                break
                
        return suggestions
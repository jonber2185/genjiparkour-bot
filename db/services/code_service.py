from sqlite3 import IntegrityError
from db.enums import Difficulty
from db.entities import CodeEntity
from db.repositories import code_repository
from errors import errors

_MIN_CODE_LENGTH = 5


class CodeService:
    def __init__(self):
        self.repository = code_repository

    def get_code(self, code: str) -> CodeEntity:
        if len(code) < _MIN_CODE_LENGTH:
            raise errors.DBError.DataValidationError("워크샵 코드는 5글자 이상이어야 합니다.")
        return self.repository.find_code(code)

    def get_codes(
        self,
        user_id: int,
        map_name: str = None,
        difficulty: str = None,
        creator: str = None,
        rand: str = None,
    ) -> list[CodeEntity]:
        if rand is None and not any([map_name, difficulty, creator]):
            raise errors.DBError.DataValidationError(
                "`전장`, `난이도`, `제작자` 중 **최소 하나 이상**은 입력해야 합니다."
            )
        return self.repository.select(int(user_id), map_name, difficulty, creator, rand)

    def add_code(
        self,
        code: str,
        map_name: str,
        difficulty: str,
        creator: str,
        cp: int = None,
        description: str = None,
        guide: str = None,
    ):
        if len(code) < _MIN_CODE_LENGTH:
            raise errors.DBError.DataValidationError("워크샵 코드는 5글자 이상이어야 합니다.")

        new_code = CodeEntity(
            code=code,
            map_name=map_name,
            difficulty=Difficulty(difficulty),
            creator=creator,
            cp=cp,
            description=description,
            guide=guide,
        )
        try:
            self.repository.insert(new_code)
        except IntegrityError as e:
            if "FOREIGN KEY" in str(e):
                raise errors.DBError.DataValidationError(
                    f"맵 '{new_code.map_name}'은(는) 등록되지 않은 맵 이름입니다."
                )
            raise errors.DBError.DuplicateError(f"코드 '{new_code.code}'가 이미 존재합니다.")

    def update_code(self, code: str, updates: dict):
        if len(code) < _MIN_CODE_LENGTH:
            raise errors.DBError.DataValidationError("워크샵 코드는 5글자 이상이어야 합니다.")
        if not updates:
            raise errors.DBError.DataValidationError("업데이트할 데이터가 없습니다.")
        if "code" in updates:
            raise errors.DBError.DataValidationError("코드(5자리)를 수정할 순 없습니다.")
        if self.repository.find_code(code) is None:
            raise errors.DBError.DataValidationError(f"`{code}` 는 없는 코드입니다.")

        try:
            self.repository.update(code, updates)
        except IntegrityError as e:
            if "FOREIGN KEY" in str(e):
                raise errors.DBError.DataValidationError(
                    f"맵 '{updates['map_name']}'은(는) 등록되지 않은 맵 이름입니다."
                )
            raise

    def delete_code(self, code: str):
        if len(code) < _MIN_CODE_LENGTH:
            raise errors.DBError.DataValidationError("워크샵 코드는 5글자 이상이어야 합니다.")
        if self.repository.find_code(code) is None:
            raise errors.DBError.DataValidationError(f"`{code}` 는 없는 코드입니다.")

        self.repository.delete(code.upper())
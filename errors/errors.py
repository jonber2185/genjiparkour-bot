class AppError(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class AuthError:
    class ForbiddenError(AppError):
        def __init__(self, message="권한이 없습니다. 관리자에게 문의하세요.", status_code=403):
            super().__init__(message, status_code)

    class UserBlockedError(AppError):
        def __init__(self, message="익명채팅에서 차단된 유저입니다.", status_code=403):
            super().__init__(message, status_code)


class DBError:
    class DataValidationError(AppError):
        def __init__(self, message="유효하지 않은 데이터입니다.", status_code=400):
            super().__init__(message, status_code)

    class DuplicateError(AppError):
        def __init__(self, message="이미 존재하는 데이터입니다.", status_code=409):
            super().__init__(message, status_code)

    class WrongApproach(AppError):
        def __init__(self, message="잘못된 접근방식입니다.", status_code=400):
            super().__init__(message, status_code)


class MessageError:
    class MessageNotFoundError(AppError):
        def __init__(self, message="메시지를 찾을 수 없습니다.", status_code=404):
            super().__init__(message, status_code)

    class SendFailedError(AppError):
        def __init__(self, message="메시지를 보내지 못했습니다.", status_code=400):
            super().__init__(message, status_code)
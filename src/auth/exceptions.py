from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    """Base class for all exceptions raised by the auth module."""
    def __init__(self, message: str, status_code: int = status.HTTP_401_UNAUTHORIZED, headers: dict = None):
        super().__init__(status_code=status_code, detail=message, headers=headers)


class InvalidCredentialsException(CredentialsException):
    """Raised when the credentials provided are invalid."""
    def __init__(self, message: str = "Invalid credentials", status_code: int = status.HTTP_401_UNAUTHORIZED, headers: dict = None):
        super().__init__(message=message, status_code=status_code, headers=headers)


class InactiveUserException(HTTPException):
    """Raised when the user is inactive."""
    def __init__(self, message: str = "Inactive user", status_code: int = status.HTTP_400_BAD_REQUEST, headers: dict = None):
        super().__init__(status_code=status_code, detail=message, headers=headers)

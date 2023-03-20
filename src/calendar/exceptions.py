from fastapi import HTTPException, status


class CalendarException(HTTPException):
    """Base class for all exceptions raised by the calendar module."""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, headers: dict = None):
        super().__init__(status_code=status_code, detail=message, headers=headers)


class CalendarNotFoundException(CalendarException):
    """Raised when the calendar is not found."""
    def __init__(self, message: str = "Calendar not found", status_code: int = status.HTTP_404_NOT_FOUND, headers: dict = None):
        super().__init__(message=message, status_code=status_code, headers=headers)


class CalendarNameTakenException(CalendarException):
    """Raised when the calendar name is already taken."""
    def __init__(self, message: str = "Calendar name already taken", status_code: int = status.HTTP_400_BAD_REQUEST, headers: dict = None):
        super().__init__(message=message, status_code=status_code, headers=headers)

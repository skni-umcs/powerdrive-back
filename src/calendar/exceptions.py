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


class UnauthorizedCalendarException(CalendarException):
    """Raised when the user is not authorized to access the calendar."""
    def __init__(self, message: str = "Unauthorized calendar", status_code: int = status.HTTP_401_UNAUTHORIZED, headers: dict = None):
        super().__init__(message=message, status_code=status_code, headers=headers)


class EventException(HTTPException):
    """Base class for all exceptions raised by the event module."""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, headers: dict = None):
        super().__init__(status_code=status_code, detail=message, headers=headers)


class EventNotFoundException(EventException):
    """Raised when the event is not found."""
    def __init__(self, message: str = "Event not found", status_code: int = status.HTTP_404_NOT_FOUND, headers: dict = None):
        super().__init__(message=message, status_code=status_code, headers=headers)


class UnauthorizedEventException(EventException):
    """Raised when the user is not authorized to access the event."""
    def __init__(self, message: str = "Unauthorized event", status_code: int = status.HTTP_401_UNAUTHORIZED, headers: dict = None):
        super().__init__(message=message, status_code=status_code, headers=headers)


class EventAlreadyExistsException(EventException):
    """Raised when the event already exists."""
    def __init__(self, message: str = "Event already exists", status_code: int = status.HTTP_400_BAD_REQUEST, headers: dict = None):
        super().__init__(message=message, status_code=status_code, headers=headers)


class DefaultCalendarException(CalendarException):
    """Raised when the user tries to delete or update the default calendar."""
    def __init__(self, message: str = "Default calendar cannot be modified", status_code: int = status.HTTP_400_BAD_REQUEST, headers: dict = None):
        super().__init__(message=message, status_code=status_code, headers=headers)

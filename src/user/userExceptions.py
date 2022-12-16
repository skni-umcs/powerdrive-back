class UserException(Exception):
    def __init__(self, message="User data is incorrect"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(UserException):
    def __init__(self, message="User was not found"):
        self.message = message
        super().__init__(self.message)


class UsernameTakenException(UserException):
    def __init__(self, message="User with given username already exists"):
        self.message = message
        super().__init__(self.message)


class UserValidationException(UserException):
    def __init__(self, message="Given credentials are incorrect"):
        self.message = message
        super().__init__(self.message)

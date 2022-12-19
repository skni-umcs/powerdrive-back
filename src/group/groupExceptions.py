class GroupNotFoundException(Exception):
    def __init__(self, message="Group not found"):
        self.message = message
        super().__init__(self.message)


class GroupNameAlreadyExistsException(Exception):
    def __init__(self, message="Group name already exists"):
        self.message = message
        super().__init__(self.message)


class OwnerNotFoundException(Exception):
    def __init__(self, message="Owner not found"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(Exception):
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)


class NoGroupPermissionsException(Exception):
    def __init__(self, message="No group premission"):
        self.message = message
        super().__init__(self.message)
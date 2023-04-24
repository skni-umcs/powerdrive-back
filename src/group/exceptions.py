class GroupNotFoundException(Exception):
    def __init__(self, message="Group not found"):
        self.message = message
        super().__init__(self.message)


class GroupNameAlreadyExistsException(Exception):
    def __init__(self, message="Group name already exists"):
        self.message = message
        super().__init__(self.message)


class NoGroupPermissionsException(Exception):
    def __init__(self, message="No group permission"):
        self.message = message
        super().__init__(self.message)
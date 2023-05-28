class NotAuthorizedShareFileException(Exception):
    def __init__(self, message="Not authorized"):
        self.message = message
        super().__init__(self.message)


class FileNotFoundException(Exception):
    def __init__(self, message="File not found"):
        self.message = message
        super().__init__(self.message)


class ShareFileNotFoundException(Exception):
    def __init__(self, message="Share not found"):
        self.message = message
        super().__init__(self.message)
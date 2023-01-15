class FileNotFoundException(Exception):
    def __init__(self, file_id: int):
        self.file_id = file_id
        super().__init__(f"File with id {file_id} not found")


class FileAlreadyExistsException(Exception):
    def __init__(self, file_name: str):
        self.file_name = file_name
        super().__init__(f"File with name {file_name} already exists")

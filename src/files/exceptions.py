class FileNotFoundException(Exception):
    def __init__(self, file_id: int):
        self.file_id = file_id
        super().__init__(f"File with id {file_id} not found")


class FileAlreadyExistsException(Exception):
    def __init__(self, file_name: str):
        self.file_name = file_name
        super().__init__(f"File with name {file_name} already exists")


class DirectoryAlreadyExistsException(Exception):
    def __init__(self, dir_name: str):
        self.dir_name = dir_name
        super().__init__(f"Directory with name {dir_name} already exists")


class DirDeleteException(Exception):
    def __init__(self, dir_name: str):
        self.dir_name = dir_name
        super().__init__(f"Directory with name {dir_name} can't be deleted")


class DirException(Exception):
    def __init__(self, dir_name: str):
        self.dir_name = dir_name
        super().__init__(f"Directory with name {dir_name} HAS PROBLEM")


class FileIsNotDirException(Exception):
    def __init__(self, file_name: str):
        self.file_name = file_name
        super().__init__(f"File with name {file_name} is not a directory")

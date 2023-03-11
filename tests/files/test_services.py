# from src.files.service import add_file, get_by_index, update, delete_by_index, get_all, _save_file
# from src.files.schemas import FileMetadata, FileMetadataCreate, FileMetadataUpdate
# from fastapi import UploadFile
# from starlette.datastructures import
# from src.dependencies import get_db
# import os
# class TestFilesDBServicesTest:
#     """Test the files database services."""
#     db = get_db()
#     filename = "test.txt"
#     file_data = b"test\ntest"
#     def test_save_file_to_disk(self):
#         """Test that the file is saved to disk."""
#         # file_data = b"test\ntest"
#         # file_name = "test.txt"
#         file_path = save_file(self.file_data, self.filename)
#         assert os.path.isfile(file_path)
#
#
#     def test_add_file_to_db(self):
#         """Test that the file is added to the database."""
#         # file_data = b"test\ntest"
#         # file_name = "test.txt"
#         file_meta = FileMetadataCreate(name=self.filename, description="test", user_id=1, size=len(self.file_data), type="text/plain")
#         file_metadata_in_db = add(self.db, UploadFile(filename=self.filename), file_meta)
#         assert file_metadata_in_db.id == 1
#         assert file_metadata_in_db.name == "test"
#         assert file_metadata_in_db.description == "test"
#         assert file_metadata_in_db.file_name == file_name
#         assert os.path.isfile(file_metadata_in_db.path)

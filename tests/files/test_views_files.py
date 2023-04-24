from tests.test_api import client

import os
from mimetypes import MimeTypes


def test_send_file():
    mime = MimeTypes()

    print(os.listdir("."), )
    file_to_send = open("./tests/files/test.txt", "rb")
    filetype = mime.guess_type(file_to_send.name)[0]

    # list all files in current directory

    response = client.post(
        "/files/",
        files={"file": (file_to_send.name, file_to_send, filetype)},
        json={
            "filename": file_to_send.name,
            "path": "/test.txt",
            "is_dir": False,
        })

    assert response.status_code == 200
    assert response.json() == {
        "filename": file_to_send.name,
        "path": "/test.txt",
        "type": "text/plain",
    }

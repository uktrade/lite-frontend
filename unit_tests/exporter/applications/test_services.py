from django.core.files.uploadedfile import SimpleUploadedFile

from exporter.applications.services import add_document_data


def test_add_document_data_no_files(rf):
    no_files_request = rf.post("/")
    data, error = add_document_data(no_files_request)
    assert data is None
    assert error == "No files attached"


def test_add_document_data_multiple_files(rf):
    multiple_files_request = rf.post(
        "/",
        {
            "file": [
                SimpleUploadedFile("file 1", b"File 1 contents"),
                SimpleUploadedFile("file 2", b"File 2 contents"),
            ]
        },
    )
    data, error = add_document_data(multiple_files_request)
    assert data is None
    assert error == "Multiple files attached"


def test_add_document_data_single_file_no_description(rf):
    single_file_request = rf.post(
        "/",
        {
            "file": SimpleUploadedFile("file 1", b"File 1 contents"),
        },
    )
    data, error = add_document_data(single_file_request)
    assert data == {"name": "file 1", "s3_key": "file 1", "size": 0}
    assert error is None


def test_add_document_data_single_file_with_description(rf):
    single_file_request = rf.post(
        "/",
        {
            "description": "test description",
            "file": SimpleUploadedFile("file 1", b"File 1 contents"),
        },
    )
    data, error = add_document_data(single_file_request)
    assert data == {"description": "test description", "name": "file 1", "s3_key": "file 1", "size": 0}
    assert error is None

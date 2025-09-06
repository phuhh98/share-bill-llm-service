import io

from fastapi import UploadFile
import pytest

from app.dependencies.fileUpload import FileUploadValidation
from app.dtos.exceptions import BadRequestException


def test_none_file_upload():
    validator = FileUploadValidation()

    noneFile = UploadFile(
        file=io.BytesIO(b""), filename="", headers=dict([("content-type", "")]), size=0
    )

    with pytest.raises(BadRequestException) as exc_info:
        validator([noneFile])

    badRequestException = exc_info.value
    assert "No file uploaded" in badRequestException.message
    assert badRequestException.status_code == 400


def test_invalid_mimeType_config_mimeType_is_not_none():
    MIME_TYPES = ["validtype"]
    INVALID_TYPE = "invalid"
    validator = FileUploadValidation(mimeTypes=MIME_TYPES)

    noneFile = UploadFile(
        file=io.BytesIO(b"somedata"),
        filename="",
        headers=dict([("content-type", INVALID_TYPE)]),
    )

    with pytest.raises(BadRequestException) as exc_info:
        validator([noneFile])

    badRequestExeption = exc_info.value
    assert "invalid mime type" in badRequestExeption.message
    assert badRequestExeption.status_code == 400


def test_maxFileSize_exceed():
    VALID_MIME_TYPE = "validtype"
    MIME_TYPES = [VALID_MIME_TYPE]
    MAX_FILE_SIZE = 20

    validator = FileUploadValidation(mimeTypes=MIME_TYPES, maxFileSize=MAX_FILE_SIZE)

    noneFile = UploadFile(
        file=io.BytesIO(b"somedata"),
        filename="",
        headers=dict([("content-type", VALID_MIME_TYPE)]),
        size=(MAX_FILE_SIZE) * 1024 * 1024,
    )

    with pytest.raises(BadRequestException) as exc_info:
        validator([noneFile])

    badRequestExeption = exc_info.value
    assert "exceeds the maximum allowed size" in badRequestExeption.message
    assert badRequestExeption.status_code == 400


def test_valid_mimeType_and_size():
    VALID_MIME_TYPE = "validtype"
    MIME_TYPES = [VALID_MIME_TYPE]
    MAX_FILE_SIZE = 20

    validator = FileUploadValidation(mimeTypes=MIME_TYPES, maxFileSize=MAX_FILE_SIZE)

    noneFile = UploadFile(
        file=io.BytesIO(b"somedata"),
        filename="",
        headers=dict([("content-type", VALID_MIME_TYPE)]),
        size=(MAX_FILE_SIZE - 1) * 1024 * 1024,
    )

    result = validator([noneFile])

    assert result[0] == noneFile


def test_valid_input_config_mimeType_none():
    VALID_MIME_TYPE = "validtype"
    # MIME_TYPES = [VALID_MIME_TYPE]
    MAX_FILE_SIZE = 20

    validator = FileUploadValidation(maxFileSize=MAX_FILE_SIZE)

    file = UploadFile(
        file=io.BytesIO(b"somedata"),
        filename="",
        headers=dict([("content-type", VALID_MIME_TYPE)]),
        size=(MAX_FILE_SIZE - 1) * 1024 * 1024,
    )

    result = validator([file])

    assert result[0] == file


def test_valid_input_and_none_for_validator_config():
    VALID_MIME_TYPE = "validtype"
    MAX_FILE_SIZE = 20

    validator = FileUploadValidation()

    noneFile = UploadFile(
        file=io.BytesIO(b"somedata"),
        filename="",
        headers=dict([("content-type", VALID_MIME_TYPE)]),
        size=(MAX_FILE_SIZE - 1) * 1024 * 1024,
    )

    result = validator([noneFile])

    assert result[0] == noneFile

from typing import Annotated, List, Optional

from fastapi import File, UploadFile

from app.dtos import exceptions


class FileUploadValidation:
    def __init__(
        self,
        mimeTypes: Annotated[Optional[List[str]], "List of allowed mimeTypes"] = None,
        maxFileSize: Annotated[Optional[int], "max allowed file size in MB"] = None,
    ):
        self.mimeTypes = mimeTypes
        self.maxFileSize = maxFileSize * 1024 * 1024  # convert to bytes

    def __call__(self, files: Annotated[List[UploadFile], File()]):
        if files is None or len(files) == 0 or files[0].size == 0:
            raise exceptions.BadRequestException(message="No files uploaded")

        if self.mimeTypes is None and self.maxFileSize is None:
            return files

        if self.maxFileSize is not None:
            for file in files:
                if file.size > self.maxFileSize:
                    raise exceptions.BadRequestException(
                        message=f"File {file.filename} exceeds the maximum allowed size of {self.maxFileSize / (1024 * 1024)} MB"
                    )
        if self.mimeTypes is not None:
            for file in files:
                if file.content_type not in self.mimeTypes:
                    raise exceptions.BadRequestException(
                        message=f"File {file.filename} has an invalid mime type {file.content_type}. Allowed types are: {', '.join(self.mimeTypes)}"
                    )
        return files

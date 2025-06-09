from typing import Optional
from fastapi import File, UploadFile, Form
from pydantic import BaseModel, Field, HttpUrl

class CreateProjectSchema(BaseModel):
    project_name: str = Field(..., description="The name of the project")
    base_url: HttpUrl = Field(..., description="The base url of the API")
    swagger_url: Optional[HttpUrl] = None
    swagger_file: Optional[UploadFile] = None

    @classmethod
    def as_form(
        cls,
        project_name: str = Form(...),
        base_url: HttpUrl = Form(...),
        swagger_url: Optional[HttpUrl] = Form(None),
        swagger_file: Optional[UploadFile] = File(None)
    ):
        return cls(
            project_name=project_name,
            base_url=base_url,
            swagger_url=swagger_url,
            swagger_file=swagger_file
        )
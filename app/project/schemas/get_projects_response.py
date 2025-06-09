from uuid import UUID
from sqlmodel import SQLModel
from app.common.schema import BaseResponse

class Project(SQLModel):
    id: UUID
    name: str
    base_url: str

class GetProjectsResponse(BaseResponse):
    data: list[Project]
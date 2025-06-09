from uuid import UUID
from sqlmodel import SQLModel
from app.common.schema import BaseResponse


class Body(SQLModel):
    id: UUID
    name: str
    type: str
    descriptive_value: str
    required: bool


class Header(SQLModel):
    id: UUID
    name: str
    type: str
    descriptive_value: str
    required: bool


class PathParameter(SQLModel):
    id: UUID
    name: str
    descriptive_value: str

class QueryParameter(SQLModel):
    id: UUID
    name: str
    descriptive_value: str

class CodeExample(SQLModel):
    id: UUID
    language: str
    language_code: str
    code: str

class Endpoint(SQLModel):
    section_id: UUID
    name: str
    url_of_endpoint: str
    description: str
    method: str
    body: list[Body]
    headers: list[Header]
    path_parameters: list[PathParameter]
    query_parameters: list[QueryParameter]
    code_examples: list[CodeExample]

class Section(SQLModel):
    project_id: UUID
    name: str
    description: str
    endpoints: list[Endpoint]

class Project(SQLModel):
    id: UUID
    name: str
    base_url: str
    sections: list[Section]

class GetProjectResponse(BaseResponse):
    data: Project
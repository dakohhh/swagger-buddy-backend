from uuid import UUID
from typing import Optional
from pydantic import ConfigDict
from sqlmodel import Field, Relationship
from app.common.models import BaseModel


class Project(BaseModel, table=True):
    name: str =  Field(max_length=50)
    base_url: str
    sections: list["Section"] = Relationship(back_populates="project", cascade_delete=True )

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)




class Section(BaseModel, table=True):
    project_id: Optional[UUID] = Field(foreign_key="project.id", ondelete="CASCADE")
    project: Optional[Project] = Relationship(back_populates="sections")
    name: str =  Field(max_length=50)
    description: str
    endpoints: list["Endpoint"] = Relationship(back_populates="section", cascade_delete=True)



class Endpoint(BaseModel, table=True):
    section_id: Optional[UUID] = Field(foreign_key="section.id", ondelete="CASCADE")
    section: Optional[Section] = Relationship(back_populates="endpoints")
    name: str =  Field(max_length=50)
    url_of_endpoint: str
    description: str
    method: str
    body: list["Body"] = Relationship(back_populates="endpoint", cascade_delete=True)
    headers: list["Header"] = Relationship(back_populates="endpoint", cascade_delete=True)
    path_parameters: list["PathParameter"] = Relationship(back_populates="endpoint", cascade_delete=True)
    query_parameters: list["QueryParameter"] = Relationship(back_populates="endpoint", cascade_delete=True)

    code_examples: list["CodeExample"] = Relationship(back_populates="endpoint", cascade_delete=True)




class CodeExample(BaseModel, table=True):
    endpoint_id: Optional[UUID] = Field(foreign_key="endpoint.id", ondelete="CASCADE")
    endpoint: Optional[Endpoint] = Relationship(back_populates="code_examples")
    language: str
    language_code: str
    code: str




class Body(BaseModel, table=True):
    endpoint_id: Optional[UUID] = Field(foreign_key="endpoint.id", ondelete="CASCADE")
    endpoint: Optional[Endpoint] = Relationship(back_populates="body")
    name: str
    type: str
    descriptive_value: str
    required: bool



class Header(BaseModel, table=True):
    endpoint_id: Optional[UUID] = Field(foreign_key="endpoint.id", ondelete="CASCADE")
    endpoint: Optional[Endpoint] = Relationship(back_populates="headers")
    name: str
    type: str
    descriptive_value: str
    required: bool



class PathParameter(BaseModel, table=True):
    endpoint_id: Optional[UUID] = Field(foreign_key="endpoint.id", ondelete="CASCADE")
    endpoint: Optional[Endpoint] = Relationship(back_populates="path_parameters")
    name: str
    descriptive_value: str



class QueryParameter(BaseModel, table=True):
    endpoint_id: Optional[UUID] = Field(foreign_key="endpoint.id", ondelete="CASCADE")
    endpoint: Optional[Endpoint] = Relationship(back_populates="query_parameters")
    name: str
    descriptive_value: str

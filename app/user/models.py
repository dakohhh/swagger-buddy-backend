from sqlmodel import Field, Column, Boolean
from sqlalchemy.sql import expression
from app.common.models import BaseModel

class User(BaseModel, table=True):
    username: str
    email: str
    password: str
    is_active: bool = Field(default=True, sa_column=Column(Boolean, default=True, nullable=False, server_default=expression.true()))
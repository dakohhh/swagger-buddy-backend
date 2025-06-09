from uuid import UUID
from sqlmodel import Field, Column, Boolean, Relationship
from sqlalchemy.sql import expression
from app.common.models import BaseModel


class RefreshToken(BaseModel, table=True):
    question: str = Field(unique=True)
    quiz_id: UUID = Field(foreign_key="quiz.id", ondelete="CASCADE")

    quiz: Quiz = Relationship(back_populates="questions")
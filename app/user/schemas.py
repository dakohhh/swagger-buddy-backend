from pydantic import BaseModel
from typing import Optional

class CreateUserSchema(BaseModel):
    username: str
    email: str
    password: str


class UpdateUserSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

from fastapi import status
from sqlmodel import SQLModel

class BaseResponse(SQLModel):
    message: str
    status_code: int = status.HTTP_200_OK
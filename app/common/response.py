from fastapi import status
from pydantic import BaseModel
from typing import Generic, TypeVar, Sequence
from fastapi.responses import JSONResponse

T = TypeVar('T')


class HttpResponse(Generic[T], JSONResponse):
    message: str
    data: T
    status_code: int = status.HTTP_200_OK

    # def __init__(self, message: str, *,data: T =None, status_code: int = status.HTTP_200_OK):

    #     # If the data is a Pydantic model, convert it to a valid JSON object
    #     if isinstance(data, BaseModel):
    #         data = data.model_dump()

    #     elif isinstance(data, Sequence) and data and isinstance(data[0], BaseModel):
    #         data = [item.model_dump() for item in data]
            
    #     super().__init__(content={"message": message, "data": data}, status_code=status_code)
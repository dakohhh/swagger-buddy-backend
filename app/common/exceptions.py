from typing import Union
from fastapi import Request, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from slowapi.errors import RateLimitExceeded

T = Union[str, dict, list, None]

class ErrorResponse(BaseModel):
    message: str
    status_code: int
    data: T = None

class BadRequestException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    def __init__(self, message: str, data: T = None):

        error = ErrorResponse(message=message, data=data, status_code=self.status_code)

        super().__init__(status_code=self.status_code, detail=error)

class UnauthorizedException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    def __init__(self, message: str, data: T = None):

        error = ErrorResponse(message=message, data=data, status_code=self.status_code)
        super().__init__(status_code=self.status_code, detail=error)


class NotFoundException(HTTPException):
    def __init__(self, message: str):
        
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        self.message = message


class ForbiddenException(HTTPException):
    def __init__(self, message: str):

        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)


async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"status": status.HTTP_429_TOO_MANY_REQUESTS, "message": str(exc.detail), "success": False},
    )
from typing import Annotated
from fastapi import Depends
from fastapi import status as HttpStatus
from app.common.router import VersionRouter
from  app.common.response  import HttpResponse

router = VersionRouter(version="1", path="swagger", tags=["Swagger"])

@router.get("/")
async def parse_swagger_format():

    return HttpResponse("Swagger UI", data=None, status_code=HttpStatus.HTTP_200_OK)
from uuid import UUID
from typing import Annotated
from fastapi import Depends
from  fastapi import status as HttpStatus
from app.common.router import VersionRouter
from app.project.service import ProjectService
from .schemas.get_projects_response import GetProjectsResponse
from .schemas.create_project import CreateProjectSchema
from .schemas.create_project_response  import CreateProjectResponse
from .schemas.get_project_response import GetProjectResponse
from .schemas.delete_project_response import DeleteProjectResponse

router = VersionRouter(version="1", path="project", tags=["Project"])


@router.post("/", response_model=CreateProjectResponse)
async def create_project(
    project_service: Annotated[ProjectService, Depends(ProjectService)],
    form_data: CreateProjectSchema = Depends(CreateProjectSchema.as_form)
):
    
    result = await project_service.create_project(form_data)

    return CreateProjectResponse(message="Create project successfully", data=result, status_code=HttpStatus.HTTP_200_OK)


@router.get("/", response_model=GetProjectsResponse)
async def get_projects(project_service: Annotated[ProjectService, Depends(ProjectService)]):

    result  = await project_service.get_projects()

    return GetProjectsResponse(message="Get all project successfully", data=result, status_code=HttpStatus.HTTP_200_OK)


@router.get("/{project_id}", response_model=GetProjectResponse)
async def get_project(project_id: UUID, project_service: Annotated[ProjectService, Depends(ProjectService)]):

    result  = await project_service.get_project(project_id)

    return GetProjectResponse(message="Get project successfully", data=result, status_code=HttpStatus.HTTP_200_OK)



@router.delete("/{project_id}", response_model=DeleteProjectResponse)
async def delete_project(project_id: UUID, project_service: Annotated[ProjectService, Depends(ProjectService)]):

    await project_service.delete_project(project_id)

    return DeleteProjectResponse(message="Delete project successfully", status_code=HttpStatus.HTTP_200_OK)
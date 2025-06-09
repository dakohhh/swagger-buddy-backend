from uuid import UUID
from fastapi import Depends
from typing import Annotated
from .service import UserService
from app.common.router import VersionRouter
from .schemas import CreateUserSchema, UpdateUserSchema

router = VersionRouter(version="1", path="user", tags=["User"])

@router.post("/")
async def create_user(user: CreateUserSchema, user_service: Annotated[UserService, Depends(UserService)]):

    new_user = await user_service.create_user(user)

    return new_user


@router.get("/")
async def get_users(user_service: Annotated[UserService, Depends(UserService)]):

    users = await user_service.get_users()

    return users



@router.get("/{user_id}")
async def get_user(user_id: UUID, user_service: Annotated[UserService, Depends(UserService)]):

    result = await user_service.get_user(user_id)

    return result


@router.put("/{user_id}")
async def update_user(user_id: UUID, update_user_schema: UpdateUserSchema, user_service: Annotated[UserService, Depends(UserService)]):

    result = await user_service.update_user(user_id, update_user_schema)

    return result


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, user_service: Annotated[UserService, Depends(UserService)]):

    await user_service.delete_user(user_id)

    return {"message": "User deleted successfully"}

from uuid import UUID
from sqlmodel import select
from .schemas import CreateUserSchema, UpdateUserSchema
from app.user.models import User
from ..database.config import DatabaseSession
from app.common.exceptions import NotFoundException

class UserService:
    def __init__(self, session: DatabaseSession):
        self.session = session

    async def create_user(self, user: CreateUserSchema):
        user = User(
            username=user.username,
            email=user.email,
            password=user.password
        )

        new_user = await self.session.save(user)
        return new_user

    async def get_users(self):
        query = await self.session.exec(select(User))

        users = query.all()

        return users
    
    async def get_user(self, user_id: UUID):
        query = await self.session.exec(select(User).where(User.id == user_id))

        user = query.first()

        if not user:
            raise NotFoundException("User not found")

        return user

    async def update_user(self, user_id: UUID, update_user_schema: UpdateUserSchema):
        query = await self.session.exec(select(User).where(User.id == user_id))

        user = query.first()

        if not user:
            raise NotFoundException("User not found")

        if update_user_schema.username:
            user.username = update_user_schema.username

        if update_user_schema.email:
            user.email = update_user_schema.email

        if update_user_schema.password:
            user.password = update_user_schema.password

        await self.session.save(user)

        return user
    
    async def delete_user(self, user_id: UUID):
        query = await self.session.exec(select(User).where(User.id == user_id))

        user = query.first()

        if not user:
            raise NotFoundException("User not found")

        await self.session.delete(user)
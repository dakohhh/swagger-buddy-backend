from fastapi import Depends, Request
from pydantic import BaseModel
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class JwtHTTPBearer(HTTPBearer):

    async def __call__(self, request: Request):
        data = await super().__call__(request)

        print(data.credentials)

        return "Hello"
    
bearer = JwtHTTPBearer()




# async def get_current_user(request: Request, data: HTTPAuthorizationCredentials = Depends(bearer)):

#     print(data)

class Token(BaseModel):
    sub: str
    exp: int
    iat: int
    iss: str # The name of your app
    type: str # access or refresh token



class RefreshToken(Token):
    jti: str # Unique identifier of the Refresh token for blacklisting and rotating

    def get_token()-> Token:
        pass
    pass
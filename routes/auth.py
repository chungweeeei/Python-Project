from fastapi import (
    APIRouter,
    status,
    HTTPException
)

from pydantic import (
    BaseModel,
    Field
)

from repository.user.user import userRepo
from repository.user.schemas import UserInfo
from repository.exceptions import (
    BadRequest,
    RepoInternalError
)

from utils.hash import verify_password
from utils.jwt import generate_access_token

class registerUserRequest(BaseModel):

    email: str = Field(...,
                       description="The email of register user",
                       example="test@test.com")
    username: str = Field(...,
                          description="The username of register user",
                          example="tester")
    password: str = Field(...,
                          description="The password of register user",
                          example="123")
    
class loginRequest(BaseModel):

    email: str = Field(...,
                       description="The email of login user",
                       example="test@test.com")
    password: str = Field(...,
                          description="The password of login user",
                          example="123")
    
class loginResponse(BaseModel):

    token: str = Field(...,
                       description="The access token")

def init_auth_router(user_repo: userRepo) -> APIRouter:

    auth_router = APIRouter(prefix="", tags=["Authentication"])

    @auth_router.post("/v1/signup")
    def signup_new_user(user_req: registerUserRequest):

        try:
            user_repo.register_user(email=user_req.email,
                                    username=user_req.username,
                                    password=user_req.password)
        except BadRequest:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"User {user_req.email} has been already registered")
        except RepoInternalError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Unexpected error when register new user")

        return status.HTTP_200_OK
    
    @auth_router.post("/v1/login",
                      response_model=loginResponse)
    def login(login_req: loginRequest):

        # verify credential
        try:
            user: UserInfo = user_repo.get_user(email=login_req.email)
        except RepoInternalError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect user email")

        verified = verify_password(password=login_req.password,
                                   hashedPassword=user.password)
        
        if not verified:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect user password")
        
        token = generate_access_token(email=login_req.email)

        return loginResponse(token=token)

    return auth_router
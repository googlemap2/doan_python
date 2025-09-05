from fastapi import APIRouter
from fastapi.security import HTTPBearer

from app.controllers.user_controller import UserController
from app.schemas.user_schema import UserLogin

router = APIRouter(prefix="/user", tags=["user"])
security = HTTPBearer()


@router.post("/login")
def login_user(user_data: UserLogin):
    controller = UserController()
    print(user_data)
    return controller.login_user(user_data)

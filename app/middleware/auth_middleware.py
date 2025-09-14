from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from sqlalchemy.orm import Session
import logging

from app.config.database import SessionLocal
from app.utils.auth import verify_token
from app.models.user import User
from app.middleware.auth_config import (
    EXCLUDED_PATHS,
    EXCLUDED_PATHS_WITH_METHODS,
    LOG_AUTH_REQUESTS,
    ERROR_MESSAGES,
)

logger = logging.getLogger(__name__)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.excluded_paths = EXCLUDED_PATHS
        self.excluded_paths_with_methods = EXCLUDED_PATHS_WITH_METHODS

    def is_excluded_path(self, path: str, method: str) -> bool:
        if path in self.excluded_paths:
            return True

        if path in self.excluded_paths_with_methods:
            allowed_methods = self.excluded_paths_with_methods[path]
            if method.upper() in [m.upper() for m in allowed_methods]:
                return True

        for excluded_path in self.excluded_paths:
            if excluded_path.endswith("*"):
                pattern = excluded_path[:-1]
                if path.startswith(pattern):
                    return True

        for excluded_path, methods in self.excluded_paths_with_methods.items():
            if excluded_path.endswith("*"):
                pattern = excluded_path[:-1]
                if path.startswith(pattern) and method.upper() in [
                    m.upper() for m in methods
                ]:
                    return True

        return False

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method

        if LOG_AUTH_REQUESTS:
            logger.info(f"Auth check: {method} {path}")

        if self.is_excluded_path(path, method):
            if LOG_AUTH_REQUESTS:
                logger.info(f"Path excluded: {method} {path}")
            response = await call_next(request)
            return response

        if method == "OPTIONS":
            response = await call_next(request)
            return response

        try:
            authorization = request.headers.get("Authorization")

            if not authorization:
                if LOG_AUTH_REQUESTS:
                    logger.warning(f"Missing authorization header for {path}")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "success": False,
                        "message": ERROR_MESSAGES["missing_auth_header"],
                        "detail": "Missing Authorization header",
                    },
                )

            if not authorization.startswith("Bearer "):
                if LOG_AUTH_REQUESTS:
                    logger.warning(f"Invalid authorization format for {path}")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "success": False,
                        "message": ERROR_MESSAGES["invalid_auth_format"],
                        "detail": "Authorization header must start with 'Bearer '",
                    },
                )

            token = authorization.split(" ")[1]

            username = verify_token(token)
            if not username:
                if LOG_AUTH_REQUESTS:
                    logger.warning(f"Invalid token for {path}")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "success": False,
                        "message": ERROR_MESSAGES["invalid_token"],
                        "detail": "Could not validate credentials",
                    },
                )

            db: Session = SessionLocal()
            try:
                user = db.query(User).filter(User.username == username).first()
                if not user:
                    if LOG_AUTH_REQUESTS:
                        logger.warning(f"User not found for username: {username}")
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "success": False,
                            "message": ERROR_MESSAGES["user_not_found"],
                            "detail": "User associated with token does not exist",
                        },
                    )

                if user.is_active is not True or user.deleted_at is not None:
                    if LOG_AUTH_REQUESTS:
                        logger.warning(f"Inactive user attempted access: {username}")
                    return JSONResponse(
                        status_code=status.HTTP_403_FORBIDDEN,
                        content={
                            "success": False,
                            "message": ERROR_MESSAGES["inactive_user"],
                            "detail": "Your account has been deactivated",
                        },
                    )

                request.state.current_user = user
                request.state.user_id = user.id
                request.state.username = user.username

            finally:
                db.close()
            response = await call_next(request)
            return response

        except Exception as e:
            logger.error(f"Authentication middleware error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "message": ERROR_MESSAGES["internal_error"],
                    "detail": "An error occurred during authentication",
                },
            )

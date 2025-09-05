from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


class ResponseHelper:
    @staticmethod
    def success(data: Any = None, message: str = "Success") -> Any:
        return {"success": True, "message": message, "data": data}

    @staticmethod
    def error(
        message: str = "Error occurred", status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> HTTPException:
        return HTTPException(
            status_code=status_code, detail={"success": False, "message": message}
        )

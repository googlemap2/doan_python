from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


class ResponseHelper:
    @staticmethod
    def response_data(
        success: bool = True, data: Any = None, message: str = "Success"
    ) -> Any:
        return {"success": success, "message": message, "data": data}

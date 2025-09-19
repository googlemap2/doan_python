from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


class ResponseHelper:
    @staticmethod
    def response_data(
        success: bool = True,
        data: dict | list[dict] | None = None,
        message: str = "Thành công",
    ):
        """Tạo phản hồi chuẩn hóa"""
        return {"success": success, "message": message, "data": data}

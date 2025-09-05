from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


class ResponseHelper:
    """Helper class for API responses"""

    @staticmethod
    def success(data: Any = None, message: str = "Success") -> Dict[str, Any]:
        """Create success response"""
        return {"success": True, "message": message, "data": data}

    @staticmethod
    def error(
        message: str = "Error occurred", status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> HTTPException:
        """Create error response"""
        return HTTPException(
            status_code=status_code, detail={"success": False, "message": message}
        )


class PaginationHelper:
    """Helper class for pagination"""

    @staticmethod
    def paginate(query, page: int = 1, size: int = 10):
        """Apply pagination to SQLAlchemy query"""
        if page < 1:
            page = 1
        if size < 1:
            size = 10
        if size > 100:
            size = 100

        offset = (page - 1) * size
        total = query.count()
        items = query.offset(offset).limit(size).all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size,
        }


def check_exists(
    db: Session, model, field: str, value: Any, exclude_id: Optional[int] = None
):
    """Check if a record exists with given field value"""
    query = db.query(model).filter(getattr(model, field) == value)
    if exclude_id:
        query = query.filter(model.id != exclude_id)
    return query.first() is not None

# Generic type for response data
from typing import Any, Optional, TypeVar, Generic
from pydantic import BaseModel


DataT = TypeVar("DataT")


class ResponseType(BaseModel, Generic[DataT]):
    success: bool = True
    message: str = "Success"
    data: Optional[DataT] = None


class ResponseMessage(ResponseType[dict | list[dict] | None]):
    pass

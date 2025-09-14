from fastapi import APIRouter, Query
from fastapi.security import HTTPBearer
from app.controllers.inventory_controller import InventoryController
from app.schemas.inventory_schema import (
    ImportWarehouse,
    ImportWarehouseResponse,
)
from fastapi import Request
router = APIRouter(prefix="/inventory", tags=["inventory"])
security = HTTPBearer()
inventory_controller = InventoryController()


@router.post("/", response_model=ImportWarehouseResponse)
def import_warehouse(inventory_data: ImportWarehouse, request: Request):
    user_id = getattr(request.state, "user_id", None)

    return inventory_controller.import_warehouse(inventory_data, user_id)

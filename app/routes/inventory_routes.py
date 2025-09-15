from typing import Optional
from fastapi import APIRouter, Query
from fastapi.security import HTTPBearer
from app.controllers.inventory_controller import InventoryController
from app.schemas.inventory_schema import (
    ImportWarehouse,
    ImportWarehouseResponse,
    GetInventoryProductResponse,
    GetInventoryResponse,
    UpdateInventory
)
from fastapi import Request
router = APIRouter(prefix="/inventory", tags=["inventory"])
security = HTTPBearer()
inventory_controller = InventoryController()


@router.post("/", response_model=ImportWarehouseResponse)
def import_warehouse(inventory_data: ImportWarehouse, request: Request):
    user_id = getattr(request.state, "user_id", None)
    return inventory_controller.import_warehouse(inventory_data, user_id)

@router.get("/get_inventory_product/{product_id}", response_model=GetInventoryProductResponse)
def get_inventory_product(product_id: int):
    return inventory_controller.get_inventory_product(product_id=product_id)

@router.get("/")
def get_inventories(
    product_name: Optional[str] = Query(None, description="Filter by product name"),
):
    return inventory_controller.get_inventories(product_name=product_name)

@router.get("/{id}", response_model=GetInventoryResponse)
def get_inventory(id: int):
    return inventory_controller.get_inventory(id=id)

@router.put("/{id}", response_model=GetInventoryResponse)
def update_inventory(id: int, inventory_data: UpdateInventory):
    return inventory_controller.update_inventory(id=id, inventory_data=inventory_data)
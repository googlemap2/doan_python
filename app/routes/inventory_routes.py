from typing import Optional
from fastapi import APIRouter, Query
from fastapi.security import HTTPBearer
from app.controllers.inventory_controller import InventoryController
from app.schemas.inventory_schema import (
    GetInventoriesResponse,
    GetInventoryProductsResponse,
    ImportWarehouse,
    ImportWarehouseResponse,
    GetInventoryProductResponse,
    GetInventoryResponse,
    UpdateInventory,
)
from fastapi import Request

router = APIRouter(prefix="/inventory", tags=["inventory"])
security = HTTPBearer()
inventory_controller = InventoryController()


@router.post("/", response_model=ImportWarehouseResponse)
def import_warehouse(
    inventory_data: ImportWarehouse, request: Request
) -> ImportWarehouseResponse:
    user_id = getattr(request.state, "user_id", None)
    """Nhập kho sản phẩm"""
    return inventory_controller.import_warehouse(inventory_data, user_id)


@router.get(
    "/get_inventory_product/{product_id}", response_model=GetInventoryProductResponse
)
def get_inventory_product(product_id: int) -> GetInventoryProductResponse:
    """Lấy thông tin tồn kho của sản phẩm"""
    return inventory_controller.get_inventory_product(product_id=product_id)


@router.get("/get_inventory_products", response_model=GetInventoryProductsResponse)
def get_inventory_products(
    product_name: Optional[str] = Query(None), product_code: Optional[str] = Query(None)
) -> GetInventoryProductsResponse:
    """Lấy thông tin tồn kho của tất cả sản phẩm với bộ lọc tùy chọn"""
    return inventory_controller.get_inventory_products(
        product_name=product_name, product_code=product_code
    )


@router.get("/", response_model=GetInventoriesResponse)
def get_inventories(
    product_name: Optional[str] = Query(None),
    product_code: Optional[str] = Query(None),
) -> GetInventoriesResponse:
    """Lấy danh sách lịch sử nhập kho với bộ lọc tùy chọn"""
    return inventory_controller.get_inventories(
        product_name=product_name, product_code=product_code
    )


@router.get("/{id}", response_model=GetInventoryResponse)
def get_inventory(id: int) -> GetInventoryResponse:
    """Lấy thông tin lịch sử nhập kho theo id"""
    return inventory_controller.get_inventory(id=id)


@router.put("/{id}", response_model=GetInventoryResponse)
def update_inventory(
    id: int, inventory_data: UpdateInventory, request: Request
) -> GetInventoryResponse:
    """Cập nhật thông tin tồn kho"""
    user_id = getattr(request.state, "user_id", None)
    return inventory_controller.update_inventory(
        id=id, inventory_data=inventory_data, user_id=user_id
    )


@router.delete("/{id}", response_model=GetInventoryResponse)
def delete_inventory(id: int, request: Request) -> GetInventoryResponse:
    """Xóa tồn kho"""
    user_id = getattr(request.state, "user_id", None)
    return inventory_controller.delete_inventory(id=id, user_id=user_id)

from app.config.database import SessionLocal
from app.services.inventory_service import InventoryService
from app.utils.helpers import ResponseHelper
from app.schemas.inventory_schema import (
    GetInventoriesResponse,
    GetInventoryProductsResponse,
    ImportWarehouse,
    ImportWarehouseResponse,
    GetInventoryProductResponse,
    GetInventoryResponse,
)


class InventoryController:

    def __init__(self):
        self.db = SessionLocal()
        self.inventory_service = InventoryService()

    def import_warehouse(
        self, inventory_data: ImportWarehouse, user_id: int
    ) -> ImportWarehouseResponse:
        """Nhập kho sản phẩm"""
        response = self.inventory_service.import_warehouse(inventory_data, user_id)
        return response

    def get_inventory_product(self, product_id: int) -> GetInventoryProductResponse:
        """Lấy thông tin tồn kho của sản phẩm"""
        inventory = self.inventory_service.get_inventory_by_product(product_id)
        return inventory

    def get_inventory_products(
        self, product_name: str | None = None, product_code: str | None = None
    ) -> GetInventoryProductsResponse:
        """Lấy thông tin tồn kho của tất cả sản phẩm với bộ lọc tùy chọn"""
        inventories = self.inventory_service.get_inventory_products(
            product_name=product_name, product_code=product_code
        )
        return inventories

    def get_inventories(
        self, product_name: str | None = None, product_code: str | None = None
    ) -> GetInventoriesResponse:
        """Lấy danh sách lịch sử nhập kho với bộ lọc tùy chọn"""
        inventories = self.inventory_service.get_inventories(
            product_name=product_name, product_code=product_code
        )
        return inventories

    def get_inventory(self, id: int) -> GetInventoryResponse:
        """Lấy thông tin nhập kho theo id"""
        inventory = self.inventory_service.get_inventory(id=id)
        return inventory

    def update_inventory(
        self, id: int, inventory_data, user_id: int
    ) -> GetInventoryResponse:
        """Cập nhật thông tin nhập kho"""
        inventory = self.inventory_service.update_inventory(id, inventory_data, user_id)
        return inventory

    def delete_inventory(self, id: int, user_id: int) -> GetInventoryResponse:
        """Xóa thông tin nhập kho"""
        inventory = self.inventory_service.delete_inventory(id, user_id)
        return inventory

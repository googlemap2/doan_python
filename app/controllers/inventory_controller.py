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
        response = self.inventory_service.import_warehouse(inventory_data, user_id)
        return response

    def get_inventory_product(self, product_id: int) -> GetInventoryProductResponse:
        inventory = self.inventory_service.get_inventory_by_product(product_id)
        return inventory

    def get_inventory_products(self) -> GetInventoryProductsResponse:
        inventories = self.inventory_service.get_inventory_products()
        return inventories

    def get_inventories(
        self, product_name: str | None = None
    ) -> GetInventoriesResponse:
        inventories = self.inventory_service.get_inventories(product_name=product_name)
        return inventories

    def get_inventory(self, id: int) -> GetInventoryResponse:
        inventory = self.inventory_service.get_inventory(id=id)
        return inventory

    def update_inventory(
        self, id: int, inventory_data, user_id: int
    ) -> GetInventoryResponse:
        inventory = self.inventory_service.update_inventory(id, inventory_data, user_id)
        return inventory

    def delete_inventory(self, id: int, user_id: int) -> GetInventoryResponse:
        inventory = self.inventory_service.delete_inventory(id, user_id)
        return inventory

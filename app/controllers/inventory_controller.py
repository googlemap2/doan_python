from app.config.database import SessionLocal
from app.services.inventory_service import InventoryService
from app.utils.helpers import ResponseHelper
from app.schemas.inventory_schema import (
    ImportWarehouse, 
    ImportWarehouseResponse
)

class InventoryController:

    def __init__(self):
        self.db = SessionLocal()
        self.inventory_service = InventoryService()

    def import_warehouse(self, inventory_data: ImportWarehouse, user_id: int) -> ImportWarehouseResponse:
        response = self.inventory_service.import_warehouse(inventory_data, user_id)
        return response
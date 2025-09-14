from datetime import datetime
from app.config.database import SessionLocal
from app.utils.helpers import ResponseHelper
from app.schemas.inventory_schema import (
    ImportWarehouse, 
    ImportWarehouseResponse
)
from app.services.product_service import ProductService
from app.models import Inventory

class InventoryService:
    def __init__(self):
        self.db = SessionLocal()
        self.product_service = ProductService()

    def import_warehouse(self, inventory_data: ImportWarehouse, user_id: int) -> ImportWarehouseResponse:
        if not self.product_service.check_product_exists(inventory_data.product_id):
            return ResponseHelper.response_data(
                success=False, message="Product does not exist"
            )
        inventory = Inventory(
            product_id=inventory_data.product_id,
            quantity=inventory_data.quantity,
            quantity_in=inventory_data.quantity,
            price=inventory_data.price,
            supplier=inventory_data.supplier,
            created_by=user_id
            
        )
        self.db.add(inventory)
        self.db.commit()
        return ResponseHelper.response_data(data=inventory.to_dict(), message="Inventory imported successfully")


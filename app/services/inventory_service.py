from datetime import datetime
from app.config.database import SessionLocal
from app.utils.helpers import ResponseHelper
from app.schemas.inventory_schema import (
    GetInventoryProductsResponse,
    ImportWarehouse,
    ImportWarehouseResponse,
    GetInventoryProductResponse,
    GetInventoriesResponse,
    GetInventoryResponse,
    UpdateInventory,
)
from app.services.product_service import ProductService
from app.models import Inventory
from app.models.product import Product


class InventoryService:
    def __init__(self):
        self.db = SessionLocal()
        self.product_service = ProductService()

    def import_warehouse(
        self, inventory_data: ImportWarehouse, user_id: int
    ) -> ImportWarehouseResponse:
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
            created_by=user_id,
        )
        self.db.add(inventory)
        self.db.commit()
        return ResponseHelper.response_data(
            data=inventory.to_dict(), message="Inventory imported successfully"
        )

    def get_inventory_by_product(self, product_id: int) -> GetInventoryProductResponse:
        inventory = (
            self.db.query(Inventory)
            .filter(Inventory.product_id == product_id)
            .filter(Inventory.deleted_at == None)
            .all()
        )
        if not inventory:
            return ResponseHelper.response_data(
                success=False, message="No inventory found for this product"
            )
        result = {
            "product_id": product_id,
            "quantity_in": sum(item.quantity_in for item in inventory),
            "total_quantity": sum(item.quantity for item in inventory),
            "product": inventory[0].product.to_dict() if inventory else None,
        }
        return ResponseHelper.response_data(
            data=result, message="Inventory fetched successfully"
        )

    def get_inventory_products(self) -> GetInventoryProductsResponse:
        inventories = (
            self.db.query(Inventory).filter(Inventory.deleted_at == None).all()
        )
        inventory_dict = {}
        for item in inventories:
            if item.product_id not in inventory_dict:
                inventory_dict[item.product_id] = {
                    "product_id": item.product_id,
                    "quantity_in": 0,
                    "total_quantity": 0,
                    "product": item.product.to_dict() if item.product else None,
                }
            inventory_dict[item.product_id]["quantity_in"] += item.quantity_in
            inventory_dict[item.product_id]["total_quantity"] += item.quantity
        result = list(inventory_dict.values())
        return ResponseHelper.response_data(
            success=True,
            message="Inventory products retrieved successfully",
            data=result,
        )

    def get_inventories(
        self, product_name: str | None = None
    ) -> GetInventoriesResponse:
        query = self.db.query(Inventory)
        query = query.filter(Inventory.deleted_at == None)
        if product_name:
            query = query.join(Inventory.product).filter(
                Product.name.ilike(f"%{product_name}%")
            )
        inventories = query.all()
        return ResponseHelper.response_data(
            success=True,
            message="Inventories retrieved successfully",
            data=[inventory.to_dict() for inventory in inventories],
        )

    def get_inventory(self, id: int) -> GetInventoryResponse:
        inventory = self.db.query(Inventory).filter(Inventory.id == id).first()
        if not inventory:
            return ResponseHelper.response_data(
                success=False, message="Inventory not found"
            )
        return ResponseHelper.response_data(
            data=inventory.to_dict(), message="Inventory fetched successfully"
        )

    def update_inventory(
        self, id: int, inventory_data: UpdateInventory, user_id: int
    ) -> GetInventoryResponse:
        inventory = (
            self.db.query(Inventory)
            .filter(Inventory.id == id)
            .filter(Inventory.deleted_at == None)
            .first()
        )
        if not inventory:
            return ResponseHelper.response_data(
                success=False, message="Inventory not found"
            )
        if inventory.quantity != inventory.quantity_in:
            return ResponseHelper.response_data(
                success=False,
                message="Cannot update inventory that has been partially used",
            )
        inventory.quantity = inventory_data.quantity
        inventory.quantity_in = inventory_data.quantity
        inventory.supplier = inventory_data.supplier
        inventory.price = inventory_data.price
        inventory.updated_by = user_id
        self.db.commit()
        return ResponseHelper.response_data(
            data=inventory.to_dict(), message="Inventory updated successfully"
        )

    def delete_inventory(self, id: int, user_id: int) -> GetInventoryResponse:
        inventory = self.db.query(Inventory).filter(Inventory.id == id).first()
        if not inventory:
            return ResponseHelper.response_data(
                success=False, message="Inventory not found"
            )
        if inventory.quantity != inventory.quantity_in:
            return ResponseHelper.response_data(
                success=False,
                message="Cannot delete inventory that has been partially used",
            )
        inventory.deleted_at = datetime.now()
        inventory.deleted_by = user_id
        inventory.updated_by = user_id
        self.db.commit()
        return ResponseHelper.response_data(
            data=inventory.to_dict(), message="Inventory deleted successfully"
        )

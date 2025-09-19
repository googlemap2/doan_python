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
        """Nhập kho sản phẩm"""
        if not self.product_service.check_product_exists(inventory_data.product_id):
            return ResponseHelper.response_data(
                success=False, message="Sản phẩm không tồn tại"
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
        return ResponseHelper.response_data(data=inventory.to_dict())

    def get_inventory_by_product(self, product_id: int) -> GetInventoryProductResponse:
        """Lấy thông tin tồn kho của sản phẩm"""
        inventory = (
            self.db.query(Inventory)
            .filter(Inventory.product_id == product_id)
            .filter(Inventory.deleted_at == None)
            .all()
        )
        if not inventory:
            return ResponseHelper.response_data(
                success=False, message="Không tìm thấy tồn kho cho sản phẩm này"
            )
        result = {
            "product_id": product_id,
            "quantity_in": sum(item.quantity_in for item in inventory),
            "total_quantity": sum(item.quantity for item in inventory),
            "product": inventory[0].product.to_dict() if inventory else None,
        }
        return ResponseHelper.response_data(data=result)

    def get_inventory_products(
        self, product_name: str | None = None, product_code: str | None = None
    ) -> GetInventoryProductsResponse:
        """Lấy thông tin tồn kho của tất cả sản phẩm với bộ lọc"""
        query = self.db.query(Inventory).filter(Inventory.deleted_at == None)
        if product_name:
            query = query.join(Inventory.product).filter(
                Product.name.ilike(f"%{product_name}%")
            )
        if product_code:
            query = query.join(Inventory.product).filter(Product.code == product_code)
        inventories = query.all()

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
            data=result,
        )

    def get_inventories(
        self, product_name: str | None = None, product_code: str | None = None
    ) -> GetInventoriesResponse:
        """Lấy danh sách tất cả các lô hàng tồn kho theo bộ lọc"""
        query = self.db.query(Inventory).filter(Inventory.deleted_at == None)
        if product_name:
            query = query.join(Inventory.product).filter(
                Product.name.ilike(f"%{product_name}%")
            )
        if product_code:
            query = query.join(Inventory.product).filter(Product.code == product_code)
        inventories = query.all()
        return ResponseHelper.response_data(
            data=[inventory.to_dict() for inventory in inventories],
        )

    def get_inventory(self, id: int) -> GetInventoryResponse:
        """Lấy thông tin tồn lô hàng theo id"""
        inventory = self.db.query(Inventory).filter(Inventory.id == id).first()
        if not inventory:
            return ResponseHelper.response_data(
                success=False, message="Không tìm thấy lô hàng tồn kho"
            )
        return ResponseHelper.response_data(data=inventory.to_dict())

    def update_inventory(
        self, id: int, inventory_data: UpdateInventory, user_id: int
    ) -> GetInventoryResponse:
        """Cập nhật thông tin lô hàng tồn kho"""
        inventory = (
            self.db.query(Inventory)
            .filter(Inventory.id == id)
            .filter(Inventory.deleted_at == None)
            .first()
        )
        if not inventory:
            return ResponseHelper.response_data(
                success=False, message="Không tìm thấy lô hàng tồn kho"
            )
        if inventory.quantity != inventory.quantity_in:
            return ResponseHelper.response_data(
                success=False,
                message="Không thể cập nhật lô hàng đã được sử dụng một phần",
            )
        inventory.quantity = inventory_data.quantity
        inventory.quantity_in = inventory_data.quantity
        inventory.supplier = inventory_data.supplier
        inventory.price = inventory_data.price
        inventory.updated_by = user_id
        self.db.commit()
        return ResponseHelper.response_data(data=inventory.to_dict())

    def delete_inventory(self, id: int, user_id: int) -> GetInventoryResponse:
        """Xóa lô hàng tồn kho"""
        inventory = self.db.query(Inventory).filter(Inventory.id == id).first()
        if not inventory:
            return ResponseHelper.response_data(
                success=False, message="Không tìm thấy lô hàng tồn kho"
            )
        if inventory.quantity != inventory.quantity_in:
            return ResponseHelper.response_data(
                success=False,
                message="Không thể xóa lô hàng đã được sử dụng một phần",
            )
        inventory.deleted_at = datetime.now()
        inventory.deleted_by = user_id
        inventory.updated_by = user_id
        self.db.commit()
        return ResponseHelper.response_data(data=inventory.to_dict())

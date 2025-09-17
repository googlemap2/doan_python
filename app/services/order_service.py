from datetime import datetime
import email

from sqlalchemy import and_
from app.config.database import SessionLocal
from app.models import order_item
from app.models.inventory import Inventory
from app.models.order_item_inventory import OrderItemInventory
from app.models.product import Product
from app.utils.helpers import ResponseHelper
from app.schemas.order_schema import CreateOrder, CreateOrderResponse
from app.models.order import Order
from app.models.customer import Customer
from app.models.order_item import OrderItem
from app.services.product_service import ProductService
from uuid import uuid4


class OrderService:
    def __init__(self):
        self.db = SessionLocal()
        self.product_service = ProductService()

    def create_order(
        self, order_data: CreateOrder, user_id: int
    ) -> CreateOrderResponse:
        order_id = uuid4()
        customer = (
            self.db.query(Customer)
            .filter(Customer.phone == order_data.customer.phone)
            .first()
        )

        get_stock = self.check_stock_availability(order_data.order_item)
        if not get_stock["success"]:
            return get_stock

        fifo_deduction = self.fifo_stock_deduction(order_data.order_item)
        if not fifo_deduction["success"]:
            return fifo_deduction

        product_ids = [item.product_id for item in order_data.order_item]
        get_products = self.product_service.get_product_by_ids(product_ids)
        if len(get_products) != len(product_ids):
            return ResponseHelper.response_data(
                success=False, message="One or more products do not exist"
            )
        if not customer:
            customer = Customer(
                fullname=order_data.customer.fullname,
                phone=order_data.customer.phone,
                address=order_data.customer.address,
                email=order_data.customer.email,
                created_by=user_id,
            )
            self.db.add(customer)
            self.db.commit()
            self.db.refresh(customer)
        else:
            customer.fullname = order_data.customer.fullname
            customer.address = order_data.customer.address
            customer.email = order_data.customer.email
            customer.updated_by = user_id
            self.db.commit()
        code = f"ORD_{datetime.now().strftime('%Y%m%d%H%M%S')}_{user_id}"
        order = Order(
            id=order_id,
            code=code,
            created_by=user_id,
            customer_id=customer.id,
        )
        for item in order_data.order_item:
            if item.product_id not in [product.id for product in get_products]:
                return ResponseHelper.response_data(
                    success=False, message="One or more products do not exist"
                )
            product = next((p for p in get_products if p.id == item.product_id), None)
            order_item_id = uuid4()
            order_items = OrderItem(
                id=order_item_id,
                product_id=item.product_id,
                quantity=item.quantity,
                order_id=order.id,
                price=product.price,
            )
            self.db.add(order_items)

            for inventory_data in fifo_deduction["data"]:
                if inventory_data["product_id"] == item.product_id:
                    order_item_inventory = OrderItemInventory(
                        order_item_id=order_item_id,
                        inventory_id=inventory_data["inventory_id"],
                        quantity=inventory_data["quantity"],
                    )
                    self.db.add(order_item_inventory)

        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)

        return ResponseHelper.response_data(
            data=order.to_dict(), message="Order created successfully"
        )

    def check_stock_availability(self, order_items) -> dict:
        """Kiểm tra tồn kho có đủ cho đơn hàng không"""
        for item in order_items:
            total_stock = (
                self.db.query(Inventory.quantity)
                .filter(
                    and_(
                        Inventory.product_id == item.product_id,
                        Inventory.quantity > 0,
                        Inventory.deleted_at.is_(None),
                    )
                )
                .all()
            )

            available_quantity = sum([stock.quantity for stock in total_stock])

            if available_quantity < item.quantity:
                product = (
                    self.db.query(Product).filter(Product.id == item.product_id).first()
                )
                return ResponseHelper.response_data(
                    success=False,
                    message=f"Insufficient stock for product {product.name}.",
                )

        return ResponseHelper.response_data(success=True, message="Stock available")

    def fifo_stock_deduction(self, order_items):
        """
        Trừ tồn kho theo phương pháp FIFO (First In, First Out)
        Lấy hàng từ lô cũ nhất trước
        """
        order_item_inventories = []
        for order_item in order_items:
            remaining_quantity = order_item.quantity
            inventories = (
                self.db.query(Inventory)
                .filter(
                    and_(
                        Inventory.product_id == order_item.product_id,
                        Inventory.quantity > 0,
                        Inventory.deleted_at.is_(None),
                    )
                )
                .order_by(Inventory.created_at.asc())
                .all()
            )

            if not inventories:
                return ResponseHelper.response_data(
                    success=False,
                    message=f"No inventory found for product {order_item.product_id}",
                )

            for inventory in inventories:
                if remaining_quantity <= 0:
                    break

                quantity_to_deduct = min(remaining_quantity, inventory.quantity)

                inventory.quantity -= quantity_to_deduct
                remaining_quantity -= quantity_to_deduct

                order_item_inventories.append(
                    {
                        "product_id": order_item.product_id,
                        "inventory_id": inventory.id,
                        "quantity": quantity_to_deduct,
                    }
                )

            if remaining_quantity > 0:
                return ResponseHelper.response_data(
                    success=False,
                    message=f"Insufficient stock for product {order_item.product_id}. "
                    f"Still need {remaining_quantity} more units",
                )
        return ResponseHelper.response_data(
            success=True,
            message="Stock deducted successfully using FIFO method",
            data=order_item_inventories,
        )

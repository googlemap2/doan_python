from datetime import datetime
from app.config.database import SessionLocal
from app.utils.helpers import ResponseHelper
from app.schemas.order_schema import (CreateOrder)
from app.models.order import Order
from app.models.customer import Customer
from app.models.order_item import OrderItem
from app.services.product_service import ProductService
from uuid import uuid4
class OrderService:
    def __init__(self):
        self.db = SessionLocal()
        self.product_service = ProductService()

    def create_order(self, order_data: CreateOrder, user_id: int):
        order_id = uuid4()
        customer = self.db.query(Customer).filter(Customer.phone == order_data.customer.phone).first()
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
                created_by=user_id,
            )
            self.db.add(customer)
            self.db.commit()
            self.db.refresh(customer)
        else:
            customer.fullname = order_data.customer.fullname
            customer.address = order_data.customer.address
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
            order_items = OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                order_id=order.id,
                price=product.price
            )
            self.db.add(order_items)
        self.db.add(order)

        self.db.commit()
        self.db.refresh(order)

        return ResponseHelper.response_data(
            data=order.to_dict(), message="Order created successfully"
        )
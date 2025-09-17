from app.config.database import SessionLocal
from app.utils.helpers import ResponseHelper
from app.services.order_service import OrderService
from app.schemas.order_schema import CreateOrder


class OrderController:

    def __init__(self):
        self.db = SessionLocal()
        self.order_service = OrderService()

    def create_order(self, order_data: CreateOrder, user_id: int):
        response = self.order_service.create_order(order_data, user_id)
        return response

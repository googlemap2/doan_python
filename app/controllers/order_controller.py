from app.config.database import SessionLocal
from app.utils.helpers import ResponseHelper
from app.services.order_service import OrderService
from app.schemas.order_schema import (
    CreateOrder,
    CreateOrderResponse,
    GetOrderResponse,
    GetOrdersResponse,
    MonthlySalesReportResponse,
    UpdateOrder,
)


class OrderController:

    def __init__(self):
        self.db = SessionLocal()
        self.order_service = OrderService()

    def create_order(
        self, order_data: CreateOrder, user_id: int
    ) -> CreateOrderResponse:
        response = self.order_service.create_order(order_data, user_id)
        return response

    def get_orders(
        self,
        customer_name: str | None = None,
        order_code: str | None = None,
        product_name: str | None = None,
        product_code: str | None = None,
        username: str | None = None,
    ) -> GetOrdersResponse:
        response = self.order_service.get_orders(
            customer_name=customer_name,
            order_code=order_code,
            product_name=product_name,
            product_code=product_code,
            username=username,
        )
        return response

    def get_order(self, order_code: str) -> GetOrderResponse:
        response = self.order_service.get_order(order_code)
        return response

    def update_order(
        self, order_code: str, order_data: UpdateOrder, user_id: int
    ) -> GetOrderResponse:
        response = self.order_service.update_order(order_code, order_data, user_id)
        return response

    def get_monthly_sales_report(
        self, username: str | None, month: int, year: int
    ) -> MonthlySalesReportResponse:
        return self.order_service.get_monthly_sales_report(username, month, year)

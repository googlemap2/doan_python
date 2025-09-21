from app.config.database import SessionLocal
from app.schemas.customer_schema import (
    CustomerUpdate,
    GetCustomerResponse,
    GetCustomersResponse,
    MonthlySalesReportResponse,
)
from app.services.customer_service import CustomerService
from app.utils.helpers import ResponseHelper


class CustomerController:

    def __init__(self):
        self.db = SessionLocal()
        self.customer_service = CustomerService()

    def get_customers(
        self,
        name: str | None = None,
        phone: str | None = None,
        address: str | None = None,
        email: str | None = None,
    ) -> GetCustomersResponse:
        """Lấy danh sách khách hàng với các bộ lọc tùy chọn"""
        response = self.customer_service.get_customers(
            name=name,
            phone=phone,
            address=address,
            email=email,
        )
        return response

    def get_customer(self, phone: str) -> GetCustomerResponse:
        """Lấy thông tin khách hàng theo số điện thoại"""
        response = self.customer_service.get_customer(phone=phone)
        return response

    def update_customer(
        self, phone: str, data_update: CustomerUpdate, user_id: int
    ) -> GetCustomerResponse:
        """Cập nhật thông tin khách hàng"""
        response = self.customer_service.update_customer(
            phone=phone, data_update=data_update, user_id=user_id
        )
        return response

    def get_monthly_sales_report(
        self, month: int, year: int
    ) -> MonthlySalesReportResponse:
        """Lấy báo cáo doanh số bán hàng theo tháng"""
        return self.customer_service.get_monthly_sales_report(month, year)

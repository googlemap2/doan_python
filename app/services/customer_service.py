from datetime import datetime
from app.config.database import SessionLocal
from app.models.customer import Customer
from app.schemas.customer_schema import (
    CustomerUpdate,
    GetCustomerResponse,
    GetCustomersResponse,
    MonthlySalesReportResponse,
)
from app.utils.helpers import ResponseHelper


class CustomerService:
    def __init__(self):
        self.db = SessionLocal()

    def get_customers(
        self,
        name: str | None = None,
        phone: str | None = None,
        address: str | None = None,
        email: str | None = None,
    ) -> GetCustomersResponse:
        """Lấy danh sách khách hàng với các bộ lọc tùy chọn"""
        query = self.db.query(Customer)

        if name:
            query = query.filter(Customer.fullname.ilike(f"%{name}%"))
        if phone:
            query = query.filter(Customer.phone.ilike(f"%{phone}%"))
        if address:
            query = query.filter(Customer.address.ilike(f"%{address}%"))
        if email:
            query = query.filter(Customer.email.ilike(f"%{email}%"))

        customers = query.all()
        customer_list = [customer.to_dict() for customer in customers]

        return ResponseHelper.response_data(
            success=True,
            data=customer_list,
            message="Lấy danh sách khách hàng thành công",
        )

    def get_customer(self, phone: str) -> GetCustomerResponse:
        """Lấy thông tin khách hàng theo số điện thoại"""
        customer = self.db.query(Customer).filter(Customer.phone == phone).first()
        if not customer:
            return ResponseHelper.response_data(
                success=False,
                message=f"Không tìm thấy khách hàng có số điện thoại {phone}",
            )
        return ResponseHelper.response_data(
            success=True,
            message="Lấy thông tin khách hàng thành công",
            data=customer.to_dict(),
        )

    def update_customer(
        self, phone: str, data_update: CustomerUpdate, user_id: int
    ) -> GetCustomerResponse:
        """Cập nhật thông tin khách hàng"""
        customer = self.db.query(Customer).filter(Customer.phone == phone).first()
        if not customer:
            return ResponseHelper.response_data(
                success=False,
                message=f"Không tìm thấy khách hàng có số điện thoại {phone}",
            )
        customer.updated_by = user_id
        if data_update.fullname is not None:
            customer.fullname = data_update.fullname
        if data_update.address is not None:
            customer.address = data_update.address
        if data_update.email is not None:
            customer.email = data_update.email
        self.db.commit()
        self.db.refresh(customer)
        return ResponseHelper.response_data(
            success=True,
            message="Cập nhật thông tin khách hàng thành công",
            data=customer.to_dict(),
        )

    def get_monthly_sales_report(
        self, month: int, year: int
    ) -> MonthlySalesReportResponse:
        """Lấy báo cáo doanh số bán hàng theo tháng"""
        reports = []
        customers = self.db.query(Customer).all()
        for customer in customers:
            sales_by_product = customer.calculate_monthly_sales_by_product(month, year)
            customer_order_codes = customer.get_order_codes()
            if sales_by_product:
                reports.append(
                    {
                        "customer_name": customer.fullname,
                        "phone": customer.phone,
                        "email": customer.email,
                        "address": customer.address,
                        "sale_products": sales_by_product,
                        "total_sales": customer.calculate_monthly_sales(month, year),
                        "order_codes": customer_order_codes,
                    }
                )
        return ResponseHelper.response_data(
            success=True,
            message="Tạo báo cáo doanh số bán hàng theo tháng thành công",
            data=reports,
        )

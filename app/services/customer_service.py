from datetime import datetime
from app.config.database import SessionLocal
from app.models.customer import Customer
from app.schemas.customer_schema import GetCustomerResponse, MonthlySalesReportResponse
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
    ):
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
            success=True, data=customer_list, message="Customers retrieved successfully"
        )

    def get_customer(self, phone: str) -> GetCustomerResponse:
        customer = self.db.query(Customer).filter(Customer.phone == phone).first()
        if not customer:
            return ResponseHelper.response_data(
                success=False,
                message=f"Customer with phone {phone} not found.",
            )
        return ResponseHelper.response_data(
            success=True,
            message="Customer retrieved successfully",
            data=customer.to_dict(),
        )

    def update_customer(self, phone: str, user_id: int) -> GetCustomerResponse:
        customer = self.db.query(Customer).filter(Customer.phone == phone).first()
        if not customer:
            return ResponseHelper.response_data(
                success=False,
                message=f"Customer with phone {phone} not found.",
            )
        customer.updated_by = user_id
        self.db.commit()
        self.db.refresh(customer)
        return ResponseHelper.response_data(
            success=True,
            message="Customer updated successfully",
            data=customer.to_dict(),
        )

    def get_monthly_sales_report(
        self, month: int, year: int
    ) -> MonthlySalesReportResponse:
        reports = []
        customers = self.db.query(Customer).all()
        for customer in customers:
            sales_by_product = customer.calculate_monthly_sales_by_product(month, year)
            if sales_by_product:
                reports.append(
                    {
                        "customer_name": customer.fullname,
                        "phone": customer.phone,
                        "email": customer.email,
                        "address": customer.address,
                        "sale_products": sales_by_product,
                        "total_sales": customer.calculate_monthly_sales(month, year),
                    }
                )
        return ResponseHelper.response_data(
            success=True,
            message="Monthly sales report generated successfully",
            data=reports,
        )

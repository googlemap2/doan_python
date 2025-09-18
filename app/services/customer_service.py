from datetime import datetime
from app.config.database import SessionLocal
from app.models.customer import Customer
from app.schemas.customer_schema import GetCustomerResponse
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

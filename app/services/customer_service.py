from datetime import datetime
from app.config.database import SessionLocal
from app.models.customer import Customer
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

from app.config.database import SessionLocal
from app.schemas.customer_schema import GetCustomersResponse
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
        response = self.customer_service.get_customers(
            name=name,
            phone=phone,
            address=address,
            email=email,
        )
        return response

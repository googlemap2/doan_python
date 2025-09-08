from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.config.database import Base


class Brand(Base):

    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    products = relationship("Product", back_populates="brand")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def __repr__(self):
        return f"<Brand(id={self.id}, name='{self.name}')>"

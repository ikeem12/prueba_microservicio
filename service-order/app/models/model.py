from datetime import date
from typing import Any

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum
from ..extensions import db

class Order(db.Model):
    """
    Represents an order placed by a customer in the system.
    """

    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(db.String(100), nullable=False, index=True)
    customer_phone: Mapped[str] = mapped_column(db.String(15), nullable=False)
    customer_email: Mapped[str] = mapped_column(db.String(100), nullable=False)
    id_product: Mapped[int] = mapped_column(db.Integer, nullable=False) 
    delivery_date: Mapped[date] = mapped_column(db.Date, nullable=False, index=True, default=date.today)
    status: Mapped[str] = mapped_column(Enum('pending','recived','ready'), default='pending', nullable=False)
    total_amount: Mapped[float] = mapped_column(db.Float, nullable=False)

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the Order instance to a serializable dictionary.

        Returns:
            dict[str, Any]: Dictionary with the order data.
        """
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "customer_email": self.customer_email,
            "id_product": self.id_product,
            "delivery_date": self.delivery_date.strftime("%d-%m-%Y"),
            "status": self.status,
            "total_amount": self.total_amount
    }
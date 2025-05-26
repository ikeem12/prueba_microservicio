from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum

from ..extensions import db

class Order(db.Model):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    id_product: Mapped[int] = mapped_column(db.Integer, nullable=False) 
    status: Mapped[str] = mapped_column(Enum('pending','paid'), default='pending', nullable=False)
    total_amount: Mapped[float] = mapped_column(db.Float, nullable=False)
from datetime import date

from sqlalchemy import Integer, Float, String, Date
from sqlalchemy.orm import Mapped, mapped_column
from app import db

class Products(db.Model):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    price:  Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    updated_at: Mapped[date] = mapped_column(Date, nullable=True)
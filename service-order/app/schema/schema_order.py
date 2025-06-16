from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, EmailStr

class BaseOrderSchema(BaseModel):
    """
    Base schema for Order-related data models.

    Provides common configuration for all order schemas.
    Strips leading and trailing whitespace from string fields.
    """
    class Config:
        str_strip_whitespace: bool = True

class SchemaOrderPost(BaseOrderSchema):
    """
    Schema for creating a new order (POST request).

    Fields:
        customer_name (str): Customer's full name (1–100 characters).
        customer_phone (str): Customer's phone number (9–15 digits).
        customer_email (EmailStr): Valid email address.
        id_product (int): ID of the product to order (must be > 0).
        delivery_date (date): Date when the order should be delivered.
    """
    customer_name: str = Field(..., min_length=1, max_length=100)
    customer_phone: str = Field(..., min_length=9, max_length=15)
    customer_email: EmailStr = Field(...)
    id_product: int = Field(..., gt=0)
    delivery_date: date = Field(...)

class SchemaOrderPut(BaseOrderSchema):
    """
    Schema for updating an existing order (PUT request).

    All fields are optional to support partial updates:
        customer_name (Optional[str]): Customer's full name (1 to 100 characters).
        customer_phone (Optional[str]): Customer's phone number (9 to 15 digits).
        customer_email (Optional[EmailStr]): Valid email address.
        id_product (Optional[int]): ID of the product to update (must be > 0).
        delivery_date (Optional[date]): New delivery date.
    """
    customer_name: Optional[str] = Field(None, min_length=1, max_length=100)
    customer_phone: Optional[str] = Field(None, min_length=9, max_length=15)
    customer_email: Optional[EmailStr] = None
    id_product: Optional[int] = Field(None, gt=0)
    delivery_date: Optional[date] = None


class SchemaOrderId(BaseModel):
    """
    Schema for validating the order ID path parameter.

    Fields:
        order_id (int): Unique identifier of the order (must be > 0).
    """
    order_id: int = Field(..., gt=0)
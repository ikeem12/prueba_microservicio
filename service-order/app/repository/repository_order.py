from typing import Type, Dict, Any

from sqlalchemy.orm import scoped_session
from sqlalchemy.exc import OperationalError, ProgrammingError, SQLAlchemyError
from sqlalchemy import select

from app.models.model import Order
from app.exceptions.api_exceptions import OrderNotFoundError
from app.exceptions.database_exceptions import ConnectionError, QueryError
from app.interfaces.interfaces_repository import IOrderRepository
from app.utils.utils import converted_rowmapping_to_dict

class RepositoryOrder(IOrderRepository):
    """
    Repository class that implements "IOrderRepository" and manages data persistence and retrieval for the Order entity.

    This class allows:
    - List all existing orders from the database.
    - Retrieve a single order by ID.
    - Create a new order record.
    - Update an existing order.
    - Delete an order.

    Attributes:
        session: SQLAlchemy scoped session used to interact with the database.
        model: SQLAlchemy model class representing the Order entity.

    Error Handling:
        Each method handles and raises appropriate exceptions:
        - ConnectionError: When database connection fails.
        - QueryError: For generic SQL execution issues.
        - OrderNotFoundError: When the requested order does not exist.
    """
    def __init__(self, session: scoped_session, model: Type[Order]):
        self.session = session
        self.model = model

    def get_all_orders(self) -> list[dict[str, Any]]:
        try:
            smt = select(
                self.model.id,
                self.model.customer_name,
                self.model.id_product,
                self.model.delivery_date,
                self.model.status,
            )
            orders = self.session.execute(smt).mappings().all()
            return  converted_rowmapping_to_dict(orders)
        
        except OperationalError as e:
            raise ConnectionError("Failed to connect to the database")
        
        except (ProgrammingError, SQLAlchemyError) as e:
            raise QueryError("Database query failed") 
        
        except Exception as e:
            raise

    def get_order(self, order_id: int) -> Dict[str, Any]:
        try:
            smt = select(self.model).filter_by(id=order_id)
            order = self.session.execute(smt).scalar_one_or_none()
            if not order:
                raise OrderNotFoundError(f"Order with id {order_id} not found")
            
            return order.to_dict()
        
        except OperationalError as e:
            raise ConnectionError("Failed to connect to the database")
        
        except (ProgrammingError, SQLAlchemyError) as e:
            raise QueryError("Database query failed") 
        
        except Exception as e:
            raise 

    def add_Order(self, order_data: Dict[str, Any]) -> bool:
        try:
            new_order = self.model(**order_data)
            self.session.add(new_order)
            self.session.commit()

            return True
        
        except OperationalError as e:
            raise ConnectionError("Failed to connect to the database")
        
        except (ProgrammingError, SQLAlchemyError) as e:
            raise QueryError("Database query failed") 
        
        except Exception as e:
            raise 

    def update_order(self, order_id: int, order_data: Dict[str, Any]) -> bool:
        try:
            smt = select(self.model).filter_by(id=order_id)
            order = self.session.execute(smt).scalars().first()

            if not order:
                raise OrderNotFoundError(f"Order with id {order_id} not found")
            
            for key, value in order_data.items():
                setattr(order, key, value)

            self.session.commit()
            return True

        except OperationalError as e:
            raise ConnectionError("Failed to connect to the database")
        
        except (ProgrammingError, SQLAlchemyError) as e:
            raise QueryError("Database query failed") 
        
        except Exception as e:
            raise

    def delete_order(self, order_id: int) -> bool:
        try:
            smt = select(self.model).filter_by(id=order_id)
            order = self.session.execute(smt).scalar_one_or_none()

            if not order:
                raise OrderNotFoundError(f"Order with id {order_id} not found")
            
            self.session.delete(order)
            self.session.commit()
            return True

        except OperationalError as e:
            raise ConnectionError("Failed to connect to the database")
        
        except (ProgrammingError, SQLAlchemyError) as e:
            raise QueryError("Database query failed") 
        
        except Exception as e:
            raise 
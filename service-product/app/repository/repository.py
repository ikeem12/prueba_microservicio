from logging import Logger
from typing import Dict, List, Any

from sqlalchemy.orm import Session
from sqlalchemy import select

from ..models.model import Products
from ..interfaces.interfaces_repository import IRepository

class Repository(IRepository):
    """"Generic repository class for CRUD operations."""
    def __init__(self, session: Session, model: Products, logger: Logger):
        self.session = session
        self.model = model
        self.logger = logger.getChild('repository')

    def get(self, offset: int, limit: int ) -> List[Dict[str, Any]]:
        """Fetches a list of items from the database with pagination.
        
        Args:
            offset (int): The starting point for fetching items.
            limit (int): The maximum number of items to fetch.  

        Returns:
            list[Dict[str,T]]: A list of items fetched from the database.
        """
        try:
            stmt = select(
                self.model.id, 
                self.model.name, 
                self.model.description,
                self.model.price,
                self.model.quantity_unit).offset(offset).limit(limit)
            result = self.session.execute(stmt).mappings().all()

            return result
        except Exception as e:
            self.session.rollback()
            self.logger.error("Error fetching products: %s", str(e), exc_info=True)
            raise

    def add(self, data: dict[str,any]) -> bool:
        try:
            item = self.model(**data)
            self.session.add(item)
            self.session.commit()
            self.logger.debug(f"Item added: {item}")
            return True
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error adding item: {e}", exc_info=True)
            return False

    def update(self, id, item):
        return self.db.update(id, item)

    def delete(self, id: int) -> bool:
        try:
            stmt = select(self.model).where(self.model.id == id)
            item = self.session.execute(stmt).scalar_one_or_none()
            
            if item:
                self.session.delete(item)
                self.session.commit()
                return True
            
            return False
        except Exception as e:
            self.session.rollback()

            return False
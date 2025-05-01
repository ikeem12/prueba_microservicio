from typing import TypeVar, Generic, Type, Dict

from sqlalchemy.orm import Session
from sqlalchemy import select

T = TypeVar('T')

class Repository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def get(self, offset: int, limit: int ) -> list[Dict[str,T]]:
        try:
            stmt = select(
                self.model.id, 
                self.model.name, 
                self.model.description,
                self.model.price).offset(offset).limit(limit)
            result = self.session.execute(stmt).all()
            return result
        except Exception as e:
            self.session.rollback()
            print(f"Error fetching items: {e}")
            raise

    def add(self, data: dict[str,any]) -> bool:
        try:
            item = self.model(**data)
            self.session.add(item)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error adding item: {e}")
            return False

    # def update(self, id, item):
    #     return self.db.update(id, item)

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
            print(f"Error deleting item: {e}")
            return False
from abc import ABC, abstractmethod
from typing import Dict, List, Any

class IRepository(ABC):
    @abstractmethod
    def get(self, offset: int, limit: int) -> list[Dict[str, Any]]:
        """Get all items with pagination."""
        pass

    @abstractmethod
    def add(self, item_data: Dict) -> bool:
        """Add a new item."""
        pass

    @abstractmethod
    def update(self, item_id: int, item_data: Dict) -> bool:
        """Update an existing item."""
        pass

    @abstractmethod
    def delete(self, item_id: int) -> bool:
        """Delete an item."""
        pass
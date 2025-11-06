"""
Base implementation for in-memory repositories
Provides common CRUD logic that all repositories can inherit
"""
from typing import Optional, TypeVar, Generic

T = TypeVar('T')


class InMemoryRepositoryBase(Generic[T]):
    """
    Base class for in-memory repository implementations.
    Provides common CRUD operations using a dictionary for storage.
    """
    
    def __init__(self) -> None:
        """Initialize with empty storage"""
        self._storage: dict[str, T] = {}
    
    def add(self, entity: T) -> None:
        """Add a new entity"""
        entity_id = self._get_entity_id(entity)
        self._storage[entity_id] = entity
    
    def get(self, entity_id: str) -> Optional[T]:
        """Retrieve an entity by ID"""
        return self._storage.get(entity_id)
    
    def update(self, entity: T) -> None:
        """Update an existing entity"""
        entity_id = self._get_entity_id(entity)
        self._storage[entity_id] = entity
    
    def delete(self, entity_id: str) -> None:
        """Remove an entity"""
        if entity_id in self._storage:
            del self._storage[entity_id]
    
    def get_all(self) -> dict[str, T]:
        """Get all entities"""
        return self._storage.copy()
    
    def exists(self, entity_id: str) -> bool:
        """Check if an entity exists"""
        return entity_id in self._storage
    
    def _get_entity_id(self, entity: T) -> str:
        """
        Extract entity ID from entity object.
        Must be overridden by subclasses if entity has different ID attribute.
        """
        # Default assumes entity has an 'id' or similar attribute
        if hasattr(entity, 'product_id'):
            return str(entity.product_id)
        elif hasattr(entity, 'customer_id'):
            return str(entity.customer_id)
        elif hasattr(entity, 'order_id'):
            return str(entity.order_id)
        elif hasattr(entity, 'supplier_id'):
            return str(entity.supplier_id)
        elif hasattr(entity, 'promo_code'):
            return str(entity.promo_code)
        else:
            raise NotImplementedError("Subclass must override _get_entity_id()")

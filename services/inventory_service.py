"""Inventory Service - Manages inventory and stock operations."""

from typing import Optional
import datetime
from domain.models.product import Product


class InventoryService:
    """Service for inventory management operations."""

    def __init__(self, product_service) -> None:
        """
        Initialize the inventory service.

        Args:
            product_service: ProductService instance for product lookups
        """
        self.__product_service = product_service
        self.__inventory_logs: list[dict] = []

    def log_inventory_change(
        self,
        product_id: str,
        quantity_change: int,
        reason: str
    ) -> None:
        """
        Log an inventory change event.

        Args:
            product_id: The product identifier
            quantity_change: The quantity change (positive or negative)
            reason: Reason for the change (e.g., 'initial_stock', 'restock', 'sale')
        """
        self.__inventory_logs.append({
            'product_id': product_id,
            'quantity_change': quantity_change,
            'reason': reason,
            'timestamp': datetime.datetime.now()
        })

    def restock_product(
        self,
        product_id: str,
        quantity: int,
        supplier_id: Optional[str] = None
    ) -> bool:
        """
        Restock a product.

        Args:
            product_id: The product identifier
            quantity: Quantity to add
            supplier_id: Optional supplier ID for verification

        Returns:
            True if successful, False otherwise
        """
        product = self.__product_service.get_product(product_id)
        if not product:
            print("Product not found")
            return False

        # Verify supplier if provided
        if supplier_id and product.supplier_id != supplier_id:
            print("Supplier mismatch")
            return False

        # Update quantity through product service
        new_quantity = product.quantity_available + quantity
        self.__product_service.update_product_quantity(product_id, new_quantity)
        
        self.log_inventory_change(product_id, quantity, "restock")
        print(f"Restocked {product.name} by {quantity}. New stock: {new_quantity}")
        return True

    def get_low_stock_products(self, threshold: int = 10) -> list[Product]:
        """
        Get all products with stock below threshold.

        Args:
            threshold: The stock threshold (default: 10)

        Returns:
            List of products with low stock
        """
        low_stock = []
        for product in self.__product_service.get_all_products().values():
            if product.quantity_available <= threshold:
                low_stock.append(product)
        return low_stock

    def check_product_availability(
        self,
        product_id: str,
        required_quantity: int
    ) -> bool:
        """
        Check if a product has sufficient stock.

        Args:
            product_id: The product identifier
            required_quantity: Required quantity

        Returns:
            True if available, False otherwise
        """
        product = self.__product_service.get_product(product_id)
        if not product:
            return False
        return product.quantity_available >= required_quantity

    def get_inventory_logs(self) -> list[dict]:
        """
        Get all inventory change logs.

        Returns:
            List of inventory log entries
        """
        return self.__inventory_logs.copy()

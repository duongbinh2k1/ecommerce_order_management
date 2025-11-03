"""Product Service - Manages product operations."""

from typing import Optional
from domain.models.product import Product


class ProductService:
    """Service for product management operations."""

    def __init__(self) -> None:
        """Initialize the product service."""
        self.__products: dict[str, Product] = {}

    def add_product(
        self,
        product_id: str,
        name: str,
        price: float,
        quantity: int,
        category: str,
        weight: float,
        supplier_id: str
    ) -> Product:
        """
        Add a new product to the catalog.

        Args:
            product_id: Unique product identifier
            name: Product name
            price: Product price
            quantity: Initial quantity available
            category: Product category
            weight: Product weight in kg
            supplier_id: ID of the product's supplier

        Returns:
            The created Product instance
        """
        product = Product(
            product_id=product_id,
            name=name,
            price=price,
            quantity_available=quantity,
            category=category,
            weight=weight,
            supplier_id=supplier_id
        )
        self.__products[product_id] = product
        return product

    def get_product(self, product_id: str) -> Optional[Product]:
        """
        Retrieve a product by ID.

        Args:
            product_id: The product identifier

        Returns:
            The Product if found, None otherwise
        """
        return self.__products.get(product_id)

    def update_product_price(self, product_id: str, new_price: float) -> bool:
        """
        Update the price of a product.

        Args:
            product_id: The product identifier
            new_price: The new price value

        Returns:
            True if successful, False if product not found
        """
        product = self.__products.get(product_id)
        if not product:
            return False

        old_price = product.price
        # Create new product with updated price (immutability pattern)
        self.__products[product_id] = Product(
            product_id=product.product_id,
            name=product.name,
            price=new_price,
            quantity_available=product.quantity_available,
            category=product.category,
            weight=product.weight,
            supplier_id=product.supplier_id
        )
        print(f"Updated {product.name} price from ${old_price.value:.2f} to ${new_price:.2f}")
        return True

    def get_all_products(self) -> dict[str, Product]:
        """
        Get all products in the catalog.

        Returns:
            Dictionary of all products
        """
        return self.__products.copy()

    def update_product_quantity(self, product_id: str, new_quantity: int) -> bool:
        """
        Update the quantity of a product.

        Args:
            product_id: The product identifier
            new_quantity: The new quantity value

        Returns:
            True if successful, False if product not found
        """
        product = self.__products.get(product_id)
        if not product:
            return False

        # Create new product with updated quantity
        self.__products[product_id] = Product(
            product_id=product.product_id,
            name=product.name,
            price=product.price.value,  # Extract primitive from Money
            quantity_available=new_quantity,
            category=product.category,
            weight=product.weight,
            supplier_id=product.supplier_id
        )
        return True

"""Product Service - Manages product operations."""

from typing import Optional
from domain.models.product import Product
from repositories.interfaces.product_repository import ProductRepository


class ProductService:
    """Service for product management operations."""

    def __init__(self, product_repository: ProductRepository) -> None:
        """
        Initialize the product service.
        
        Args:
            product_repository: Repository for product data access (DI)
        """
        self.__repository = product_repository

    def add_product(
        self,
        product_id: int,
        name: str,
        price: float,
        quantity: int,
        category: str,
        weight: float,
        supplier_id: int
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
        self.__repository.add(product)
        # Note: Repository uses string keys internally, conversion handled by repository
        return product

    def get_product(self, product_id: int) -> Optional[Product]:
        """
        Retrieve a product by ID.

        Args:
            product_id: The product identifier

        Returns:
            The Product if found, None otherwise
        """
        return self.__repository.get(product_id)

    def update_product_price(self, product_id: int, new_price: float) -> bool:
        """
        Update the price of a product.

        Args:
            product_id: The product identifier
            new_price: The new price value

        Returns:
            True if successful, False if product not found
        """
        product = self.__repository.get(product_id)
        if not product:
            return False

        old_price = product.price
        # Create new product with updated price (immutability pattern)
        updated_product = Product(
            product_id=product.product_id,
            name=product.name,
            price=new_price,
            quantity_available=product.quantity_available,
            category=product.category,
            weight=product.weight,
            supplier_id=product.supplier_id
        )
        self.__repository.update(updated_product)
        print(
            f"Updated {product.name} price from ${old_price:.2f} to ${new_price:.2f}")
        return True

    def get_all_products(self) -> dict[int, Product]:
        """
        Get all products in the catalog.

        Returns:
            Dictionary of all products
        """
        return self.__repository.get_all()

    def update_product_quantity(self, product_id: int, new_quantity: int) -> bool:
        """
        Update the quantity of a product.

        Args:
            product_id: The product identifier
            new_quantity: The new quantity value

        Returns:
            True if successful, False if product not found
        """
        product = self.__repository.get(product_id)
        if not product:
            return False

        # Create new product with updated quantity
        updated_product = Product(
            product_id=product.product_id,
            name=product.name,
            price=product.price.value,  # Extract primitive from Money
            quantity_available=new_quantity,
            category=product.category,
            weight=product.weight,
            supplier_id=product.supplier_id
        )
        self.__repository.update(updated_product)
        return True

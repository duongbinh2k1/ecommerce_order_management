"""
Sales Report value object - immutable sales metrics data
Used by: ReportingService.generate_sales_report() return value
"""
from typing import Any


class SalesReport:
    """Value object representing sales report data."""
    
    def __init__(
        self,
        total_sales: float,
        total_orders: int,
        cancelled_orders: int,
        products_sold: dict[int, int],
        revenue_by_category: dict[str, float],
        top_customers: list[tuple[int, float]]
    ) -> None:
        """
        Initialize sales report.
        
        Args:
            total_sales: Total sales amount
            total_orders: Number of completed orders
            cancelled_orders: Number of cancelled orders
            products_sold: Product ID -> quantity sold mapping
            revenue_by_category: Category -> revenue mapping
            top_customers: List of (customer_id, lifetime_value) tuples
        """
        self.__validate(total_sales, total_orders, cancelled_orders)
        
        self.__total_sales = total_sales
        self.__total_orders = total_orders
        self.__cancelled_orders = cancelled_orders
        self.__products_sold = products_sold.copy()  # Defensive copy
        self.__revenue_by_category = revenue_by_category.copy()
        self.__top_customers = top_customers.copy()

    def __validate(
        self,
        total_sales: float,
        total_orders: int,
        cancelled_orders: int
    ) -> None:
        """Validate report data."""
        if total_sales < 0:
            raise ValueError("Total sales cannot be negative")
        if total_orders < 0:
            raise ValueError("Total orders cannot be negative")
        if cancelled_orders < 0:
            raise ValueError("Cancelled orders cannot be negative")

    @property
    def total_sales(self) -> float:
        """Get total sales amount."""
        return self.__total_sales

    @property
    def total_orders(self) -> int:
        """Get total number of completed orders."""
        return self.__total_orders

    @property
    def cancelled_orders(self) -> int:
        """Get number of cancelled orders."""
        return self.__cancelled_orders

    @property
    def products_sold(self) -> dict[int, int]:
        """Get products sold (product_id -> quantity)."""
        return self.__products_sold.copy()  # Return defensive copy

    @property
    def revenue_by_category(self) -> dict[str, float]:
        """Get revenue by category."""
        return self.__revenue_by_category.copy()

    @property
    def top_customers(self) -> list[tuple[int, float]]:
        """Get top customers by lifetime value."""
        return self.__top_customers.copy()

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary for backward compatibility.
        
        Returns:
            dict: Report data as dictionary (same format as legacy)
        """
        return {
            'total_sales': self.__total_sales,
            'total_orders': self.__total_orders,
            'cancelled_orders': self.__cancelled_orders,
            'products_sold': self.__products_sold.copy(),
            'revenue_by_category': self.__revenue_by_category.copy(),
            'top_customers': self.__top_customers.copy()
        }

    def __str__(self) -> str:
        """String representation of sales report."""
        return (
            f"Sales Report: ${self.__total_sales:.2f} revenue, "
            f"{self.__total_orders} orders, {self.__cancelled_orders} cancelled"
        )

    def __repr__(self) -> str:
        """Detailed representation of sales report."""
        return (
            f"SalesReport("
            f"total_sales={self.__total_sales}, "
            f"total_orders={self.__total_orders}, "
            f"cancelled_orders={self.__cancelled_orders})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality with another sales report."""
        if not isinstance(other, SalesReport):
            return False
        
        return (
            abs(self.__total_sales - other.total_sales) < 0.01 and
            self.__total_orders == other.total_orders and
            self.__cancelled_orders == other.cancelled_orders and
            self.__products_sold == other.products_sold and
            self.__revenue_by_category == other.revenue_by_category and
            self.__top_customers == other.top_customers
        )

    def __hash__(self) -> int:
        """Hash for using in sets/dicts."""
        return hash((
            round(self.__total_sales, 2),
            self.__total_orders,
            self.__cancelled_orders,
            tuple(sorted(self.__products_sold.items())),
            tuple(sorted(self.__revenue_by_category.items())),
            tuple(self.__top_customers)
        ))
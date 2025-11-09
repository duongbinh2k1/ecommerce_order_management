"""
Application Orchestrator - Handles dependency injection and service coordination
Replaces hardcoded dependency wiring in order_system.py
Implements proper Dependency Injection pattern as required in Phase 5
"""
import datetime
from typing import Any, Optional

from domain.models.product import Product
from domain.models.customer import Customer
from domain.models.order import Order
from domain.models.supplier import Supplier
from domain.models.promotion import Promotion
from domain.enums.shipping_method import ShippingMethod
from domain.enums.membership_tier import MembershipTier
from domain.enums.order_status import OrderStatus

# Import all repositories
from repositories import (
    InMemoryProductRepository,
    InMemoryCustomerRepository,
    InMemoryOrderRepository,
    InMemorySupplierRepository,
    InMemoryPromotionRepository,
    InMemoryShipmentRepository,
)

# Import all services
from services import (
    ProductService,
    InventoryService,
    CustomerService,
    SupplierService,
    PromotionService,
    PricingService,
    ShippingService,
    PaymentService,
    NotificationService,
    OrderService,
    ReportingService,
    MarketingService,
    ShipmentService
)


class OrderProcessor:
    """
    Application orchestrator that handles dependency injection and coordinates services.
    
    This class replaces the hardcoded dependency wiring in order_system.py
    and provides a clean, testable entry point to the application.
    """

    def __init__(self) -> None:
        """Initialize all dependencies using proper dependency injection."""
        # Initialize repositories (Data Access Layer)
        self._product_repository = InMemoryProductRepository()
        self._customer_repository = InMemoryCustomerRepository()
        self._order_repository = InMemoryOrderRepository()
        self._supplier_repository = InMemorySupplierRepository()
        self._promotion_repository = InMemoryPromotionRepository()
        self._shipment_repository = InMemoryShipmentRepository()

        # Initialize services with repository injection (Dependency Injection pattern)
        self._product_service = ProductService(self._product_repository)
        self._inventory_service = InventoryService(self._product_service)
        self._customer_service = CustomerService(self._customer_repository)
        self._supplier_service = SupplierService(self._supplier_repository)
        self._promotion_service = PromotionService(self._promotion_repository)
        self._pricing_service = PricingService()
        self._shipping_service = ShippingService()
        self._shipment_service = ShipmentService(self._shipment_repository)
        self._payment_service = PaymentService()
        self._notification_service = NotificationService()

        self._order_service = OrderService(
            order_repository=self._order_repository,
            product_service=self._product_service,
            customer_service=self._customer_service,
            pricing_service=self._pricing_service,
            payment_service=self._payment_service,
            shipping_service=self._shipping_service,
            shipment_service=self._shipment_service,
            notification_service=self._notification_service,
            inventory_service=self._inventory_service,
            promotion_service=self._promotion_service
        )

        self._reporting_service = ReportingService(
            customer_service=self._customer_service,
            order_service=self._order_service,
            product_service=self._product_service
        )

        self._marketing_service = MarketingService(
            customer_service=self._customer_service,
            order_service=self._order_service
        )

    # Public API methods for application operations

    def add_product(self, product_id: int, name: str, price: float, quantity: int,
                    category: str, weight: float, supplier_id: int) -> Product:
        """Add a product to the catalog."""
        product = self._product_service.add_product(
            product_id, name, price, quantity, category, weight, supplier_id
        )
        self._inventory_service.log_inventory_change(
            product_id, quantity, "initial_stock")
        return product

    def add_customer(self, customer_id: int, name: str, email: str, tier: str,
                     phone: str, address: str) -> Customer:
        """Add a customer to the system."""
        # Convert string to enum at the boundary
        tier_enum = MembershipTier(tier)
        return self._customer_service.add_customer(
            customer_id, name, email, tier_enum, phone, address
        )

    def add_supplier(self, supplier_id: int, name: str, email: str, reliability: float) -> Supplier:
        """Add a supplier to the system."""
        return self._supplier_service.add_supplier(
            supplier_id, name, email, reliability
        )

    def add_promotion(self, promo_id: int, code: str, discount: float,
                      min_purchase: float, valid_until: datetime.datetime, category: str) -> Promotion:
        """Add a promotion to the system."""
        return self._promotion_service.add_promotion(
            promo_id, code, discount, min_purchase, valid_until, category
        )

    def process_order(self, customer_id: int, order_items: list[Any], payment_info: dict[str, Any],
                      promo_code: Optional[str] = None, shipping_method: str = 'standard') -> Optional[Order]:
        """Process an order through the system."""
        # Convert string to enum at the boundary
        shipping_method_enum = ShippingMethod(shipping_method)
        
        # Convert order_items to expected format
        order_items_tuples = []
        for item in order_items:
            order_items_tuples.append(
                (item.product_id, item.quantity, item.unit_price))

        order = self._order_service.create_order(
            customer_id=customer_id,
            order_items=order_items_tuples,
            payment_info=payment_info,
            promo_code=promo_code,
            shipping_method=shipping_method_enum
        )
        
        if order:
            # Check low stock and notify suppliers
            for product_id, _, _ in order_items_tuples:
                product = self._product_service.get_product(product_id)
                if product and product.quantity_available < 5:
                    self._supplier_service.notify_reorder(
                        product_name=product.name,
                        supplier_id=product.supplier_id,
                        current_stock=product.quantity_available
                    )
        
        return order

    def update_order_status(self, order_id: int, new_status: str) -> Optional[Order]:
        """Update order status."""
        # Convert string to enum at the boundary
        status_enum = OrderStatus(new_status)
        return self._order_service.update_order_status(order_id, status_enum)

    def get_low_stock_products(self, threshold: int) -> list[Product]:
        """Get products with low stock."""
        return self._inventory_service.get_low_stock_products(threshold)

    def generate_sales_report(self, start_date: datetime.datetime, end_date: datetime.datetime) -> dict[str, Any]:
        """Generate sales report."""
        return self._reporting_service.generate_sales_report(start_date, end_date)

    def get_customer_lifetime_value(self, customer_id: int) -> float:
        """Get customer lifetime value."""
        return self._reporting_service.get_customer_lifetime_value(customer_id)

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """Get customer by ID."""
        return self._customer_service.get_customer(customer_id)

    @property
    def product_service(self) -> ProductService:
        return self._product_service

    @property
    def customer_service(self) -> CustomerService:
        return self._customer_service

    @property
    def order_service(self) -> OrderService:
        return self._order_service

    @property
    def inventory_service(self) -> InventoryService:
        return self._inventory_service

    @property
    def reporting_service(self) -> ReportingService:
        return self._reporting_service

    @property
    def marketing_service(self) -> MarketingService:
        return self._marketing_service

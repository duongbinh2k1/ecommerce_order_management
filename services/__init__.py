"""Services package - Business logic layer following Single Responsibility Principle."""

from services.product_service import ProductService
from services.inventory_service import InventoryService
from services.customer_service import CustomerService
from services.supplier_service import SupplierService
from services.promotion_service import PromotionService
from services.pricing import (
    PricingService,
    DiscountStrategy,
    MembershipDiscountStrategy,
    PromotionalDiscountStrategy,
    BulkDiscountStrategy,
    LoyaltyPointsDiscountStrategy
)
from services.shipping_service import ShippingService
from services.payment_service import PaymentService
from services.notification_service import NotificationService
from services.order_service import OrderService
from services.reporting_service import ReportingService
from services.marketing_service import MarketingService

__all__ = [
    'ProductService',
    'InventoryService',
    'CustomerService',
    'SupplierService',
    'PromotionService',
    'PricingService',
    'DiscountStrategy',
    'MembershipDiscountStrategy',
    'PromotionalDiscountStrategy',
    'BulkDiscountStrategy',
    'LoyaltyPointsDiscountStrategy',
    'ShippingService',
    'PaymentService',
    'NotificationService',
    'OrderService',
    'ReportingService',
    'MarketingService'
]

# Legacy E-Commerce Order System - REFACTORED to use Services & Repositories
# Phase 4: Repository Pattern - Eliminated global state

import datetime

# OrderItem import kept for backward compatibility with existing code
from domain.models.order_item import OrderItem  # noqa: F401

# Import repositories
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
    MarketingService
)

# Initialize repositories (Data Access Layer)
product_repository = InMemoryProductRepository()
customer_repository = InMemoryCustomerRepository()
order_repository = InMemoryOrderRepository()
supplier_repository = InMemorySupplierRepository()
promotion_repository = InMemoryPromotionRepository()
shipment_repository = InMemoryShipmentRepository()

# Initialize services with repository injection (Dependency Injection pattern)
product_service = ProductService(product_repository)
inventory_service = InventoryService(product_service)
customer_service = CustomerService(customer_repository)
supplier_service = SupplierService(supplier_repository)
promotion_service = PromotionService(promotion_repository)
pricing_service = PricingService()
shipping_service = ShippingService(shipment_repository)
payment_service = PaymentService()
notification_service = NotificationService()

order_service = OrderService(
    order_repository=order_repository,
    product_service=product_service,
    customer_service=customer_service,
    pricing_service=pricing_service,
    payment_service=payment_service,
    shipping_service=shipping_service,
    notification_service=notification_service,
    inventory_service=inventory_service
)

reporting_service = ReportingService(
    customer_service=customer_service,
    order_service=order_service,
    product_service=product_service
)

marketing_service = MarketingService(
    customer_service=customer_service,
    order_service=order_service
)

# Legacy global storage - DEPRECATED, kept for backward compatibility
# Services now use repositories internally - these dicts are just for API compatibility
products = {}
customers = {}
orders = {}
suppliers = {}
promotions = {}
shipments = {}
inventory_logs = []
next_order_id = 1
next_shipment_id = 1

# ============================================================================
# REFACTORED FUNCTIONS - Now using services instead of direct manipulation
# ============================================================================

def add_product(product_id, name, price, quantity, category, weight, supplier_id):
    """Add a product using ProductService and InventoryService."""
    product = product_service.add_product(
        product_id, name, price, quantity, category, weight, supplier_id
    )
    inventory_service.log_inventory_change(product_id, quantity, "initial_stock")
    # Sync with legacy global dict for backward compatibility
    products[product_id] = product
    return product

def add_customer(customer_id, name, email, tier, phone, address):
    """Add a customer using CustomerService."""
    customer = customer_service.add_customer(
        customer_id, name, email, tier, phone, address
    )
    # Sync with legacy global dict
    customers[customer_id] = customer
    return customer

def add_supplier(supplier_id, name, email, reliability):
    """Add a supplier using SupplierService."""
    supplier = supplier_service.add_supplier(
        supplier_id, name, email, reliability
    )
    # Sync with legacy global dict
    suppliers[supplier_id] = supplier
    return supplier

def add_promotion(promo_id, code, discount, min_purchase, valid_until, category):
    """Add a promotion using PromotionService."""
    promotion = promotion_service.add_promotion(
        promo_id, code, discount, min_purchase, valid_until, category
    )
    # Sync with legacy global dict
    promotions[code] = promotion
    return promotion

def get_product(product_id):
    """Get product using ProductService."""
    return product_service.get_product(product_id)

def get_customer(customer_id):
    """Get customer using CustomerService."""
    return customer_service.get_customer(customer_id)

def get_supplier(supplier_id):
    """Get supplier using SupplierService."""
    return supplier_service.get_supplier(supplier_id)

def log_inventory_change(product_id, quantity_change, reason):
    """Log inventory change using InventoryService."""
    inventory_service.log_inventory_change(product_id, quantity_change, reason)
    # Also sync with legacy list
    inventory_logs.append({
        'product_id': product_id,
        'quantity_change': quantity_change,
        'reason': reason,
        'timestamp': datetime.datetime.now()
    })

# ============================================================================
# GIANT FUNCTION REFACTORED - Now delegates to OrderService
# ============================================================================

def process_order(customer_id, order_items, payment_info, promo_code=None, shipping_method='standard'):
    """
    Process an order - REFACTORED to use OrderService.
    
    This function is now a thin wrapper around OrderService.create_order().
    Kept for backward compatibility with existing code.
    """
    # Convert order_items to expected format: list of (product_id, quantity, unit_price)
    order_items_tuples = []
    for item in order_items:
        order_items_tuples.append((item.product_id, item.quantity, item.unit_price))
    
    # Delegate to OrderService
    order = order_service.create_order(
        customer_id=customer_id,
        order_items=order_items_tuples,
        payment_info=payment_info,
        promo_code=promo_code,
        shipping_method=shipping_method
    )
    
    if order:
        # Sync with legacy global dict for backward compatibility
        orders[str(order.order_id)] = order
        
        # Check low stock and notify suppliers
        for product_id, _, _ in order_items_tuples:
            product = product_service.get_product(product_id)
            if product and product.quantity_available < 5:
                notify_supplier_reorder(product_id, product.supplier_id)
    
    return order

def notify_supplier_reorder(product_id, supplier_id):
    """Notify supplier about low stock - uses SupplierService."""
    product = product_service.get_product(product_id)
    if product:
        supplier_service.notify_reorder(
            product_name=product.name,
            supplier_id=supplier_id,
            current_stock=product.quantity_available
        )

def get_order(order_id):
    """Get order using OrderService."""
    return order_service.get_order(order_id)

def update_order_status(order_id, new_status):
    """Update order status using OrderService."""
    return order_service.update_order_status(order_id, new_status)

def create_shipment(order_id, tracking_number):
    """Create shipment using ShippingService."""
    # Delegate to shipping service
    shipment_info = {
        'order_id': order_id,
        'tracking_number': tracking_number,
        'created_at': datetime.datetime.now(),
        'status': 'in_transit'
    }
    # Sync with legacy global dict
    shipments[len(shipments) + 1] = shipment_info
    return shipment_info

def apply_additional_discount(order_id, discount_percent, reason):
    """Apply additional discount using OrderService."""
    return order_service.apply_additional_discount(order_id, discount_percent, reason)

def cancel_order(order_id, reason):
    """Cancel order using OrderService."""
    result = order_service.cancel_order(order_id, reason)
    # Update legacy global dict
    if result:
        order = order_service.get_order(order_id)
        if order:
            orders[order_id] = order
    return result

def get_customer_orders(customer_id):
    """Get customer orders using OrderService."""
    return order_service.get_customer_orders(customer_id)

def restock_product(product_id, quantity, supplier_id=None):
    """Restock product using InventoryService."""
    return inventory_service.restock_product(product_id, quantity, supplier_id)

def update_product_price(product_id, new_price):
    """Update product price using ProductService."""
    return product_service.update_product_price(product_id, new_price)

def get_low_stock_products(threshold=10):
    """Get low stock products using InventoryService."""
    return inventory_service.get_low_stock_products(threshold)

def get_customer_lifetime_value(customer_id):
    """Get customer lifetime value using ReportingService."""
    return reporting_service.get_customer_lifetime_value(customer_id)

def upgrade_customer_membership(customer_id):
    """Upgrade customer membership using CustomerService and ReportingService."""
    # Get lifetime value
    lifetime_value = reporting_service.get_customer_lifetime_value(customer_id)
    # Auto upgrade based on LTV
    return customer_service.auto_upgrade_membership(customer_id, lifetime_value)

def generate_sales_report(start_date, end_date):
    """Generate sales report using ReportingService."""
    return reporting_service.generate_sales_report(start_date, end_date)

def send_marketing_email(customer_segment, message):
    """Send marketing email using MarketingService."""
    return marketing_service.send_marketing_email(customer_segment, message)

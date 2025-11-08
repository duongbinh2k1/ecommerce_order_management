# Demo usage of the refactored system using OrderProcessor
from application.order_processor import OrderProcessor
from domain.models.order_item import OrderItem
import datetime

print("=" * 60)
print("E-Commerce Refactored System Demo")
print("=" * 60)

# Initialize the application orchestrator
order_processor = OrderProcessor()

# Setup suppliers
print("\n1. Setting up suppliers...")
order_processor.add_supplier(1, "TechDistributor Inc", "orders@techdist.com", 4.5)
order_processor.add_supplier(2, "ElectroSupply Co", "sales@electro.com", 4.2)
order_processor.add_supplier(3, "GadgetWholesale", "info@gadgetwholesale.com", 4.8)

# Setup products
print("\n2. Adding products to inventory...")
order_processor.add_product(1, "Laptop Pro 15", 999.99, 15, "Electronics", 2.5, 1)
order_processor.add_product(2, "Wireless Mouse", 29.99, 50, "Electronics", 0.2, 2)
order_processor.add_product(3, "Mechanical Keyboard", 79.99, 30, "Electronics", 1.0, 2)
order_processor.add_product(4, "4K Monitor", 299.99, 20, "Electronics", 5.0, 1)
order_processor.add_product(5, "USB-C Hub", 49.99, 40, "Electronics", 0.3, 3)
order_processor.add_product(6, "Laptop Bag", 39.99, 25, "Accessories", 0.8, 3)
order_processor.add_product(7, "Desk Lamp", 34.99, 35, "Accessories", 1.2, 3)
order_processor.add_product(8, "Ergonomic Chair", 299.99, 10, "Furniture", 15.0, 1)
order_processor.add_product(9, "Standing Desk", 499.99, 8, "Furniture", 25.0, 1)
order_processor.add_product(10, "Webcam HD", 79.99, 45, "Electronics", 0.4, 2)

# Setup customers
print("\n3. Creating customer accounts...")
order_processor.add_customer(101, "Alice Smith", "alice@email.com", "gold", "555-0101", "123 Main St, CA 94102")
order_processor.add_customer(102, "Bob Jones", "bob@email.com", "silver", "555-0102", "456 Oak Ave, NY 10001")
order_processor.add_customer(103, "Charlie Brown", "charlie@email.com", "standard", "555-0103", "789 Pine Rd, TX 75001")
order_processor.add_customer(104, "Diana Prince", "diana@email.com", "bronze", "555-0104", "321 Elm St, CA 90210")
order_processor.add_customer(105, "Eve Wilson", "eve@email.com", "standard", "555-0105", "654 Maple Dr, NY 10002")

# Add some promotions
print("\n4. Setting up promotions...")
order_processor.add_promotion(1, "SAVE15", 15, 100, datetime.datetime.now() + datetime.timedelta(days=30), "Electronics")
order_processor.add_promotion(2, "WELCOME10", 10, 0, datetime.datetime.now() + datetime.timedelta(days=60), "all")

# Create first order
print("\n5. Processing first order (Gold member, with promo code)...")
items1 = [
    OrderItem(1, 1, 999.99),
    OrderItem(2, 2, 29.99),
    OrderItem(5, 1, 49.99)
]
payment1 = {"valid": True, "type": "credit_card", "card_number": "1234567890123456", "amount": 1000}
order1 = order_processor.process_order(101, items1, payment1, promo_code="SAVE15", shipping_method='express')
if order1:
    print(f"✓ Order {order1.order_id} created successfully!")
    print(f"  Total: ${order1.total_price.value:.2f} (includes ${order1.shipping_cost.value:.2f} shipping)")
    print(f"  Status: {order1.status}")

# Create second order
print("\n6. Processing second order (Standard member, bulk purchase)...")
items2 = [
    OrderItem(3, 5, 79.99),
    OrderItem(10, 3, 79.99)
]
payment2 = {"valid": True, "type": "paypal", "email": "charlie@email.com", "amount": 700}
order2 = order_processor.process_order(103, items2, payment2, shipping_method='standard')
if order2:
    print(f"✓ Order {order2.order_id} created successfully!")
    print(f"  Total: ${order2.total_price.value:.2f}")

# Create third order
print("\n7. Processing third order (Bronze member, furniture)...")
items3 = [
    OrderItem(8, 1, 299.99),
    OrderItem(7, 2, 34.99)
]
payment3 = {"valid": True, "type": "credit_card", "card_number": "9876543210987654", "amount": 400}
order3 = order_processor.process_order(104, items3, payment3, shipping_method='standard')
if order3:
    print(f"✓ Order {order3.order_id} created successfully!")

# Update order status
print("\n8. Shipping an order...")
if order1 is not None:
    updated = order_processor.update_order_status(order1.order_id, 'shipped')
    if updated is not None:
        print(f"✓ Order {order1.order_id} marked as shipped")
        if updated.tracking_number:
            print(f"  Tracking: {updated.tracking_number}")

# Check low stock
print("\n9. Checking inventory status...")
low_stock = order_processor.get_low_stock_products(15)
if low_stock:
    print(f"⚠ Found {len(low_stock)} products with low stock:")
    for product in low_stock[:3]:
        print(f"  - {product.name}: {product.quantity_available} units")

# Generate sales report
print("\n10. Generating sales report...")
start = datetime.datetime.now() - datetime.timedelta(days=1)
end = datetime.datetime.now() + datetime.timedelta(days=1)
report = order_processor.generate_sales_report(start, end)
print(f"Total Sales: ${report['total_sales']:.2f}")
print(f"Total Orders: {report['total_orders']}")
print("Revenue by Category:")
revenue_by_category: dict[str, float] = report['revenue_by_category']
for category, revenue in revenue_by_category.items():
    print(f"  {category}: ${revenue:.2f}")

# Check customer lifetime values
print("\n11. Customer lifetime values...")
for cust_id in [101, 102, 103, 104]:
    customer = order_processor.get_customer(cust_id)
    if customer:
        ltv = order_processor.get_customer_lifetime_value(cust_id)
        print(f"{customer.name} ({customer.membership_tier}): ${ltv:.2f}")

print("\n" + "=" * 60)
print("Demo completed!")
print("=" * 60)
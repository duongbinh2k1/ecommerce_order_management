# Utility to load/save data (also needs refactoring!)
import json
import datetime
from typing import Any

# Note: This file references old order_system module which no longer exists
# It should be refactored to use the new OrderProcessor architecture

def save_data_to_file(filename: str) -> None:
    # Another monolithic function doing too much
    data: dict[str, Any] = {
        'products': {},
        'customers': {},
        'orders': {},
        'suppliers': {},
        'promotions': {}
    }

    # Convert products
    # Note: This code references old global variables that no longer exist
    # This file needs refactoring to use OrderProcessor
    products: dict[str, Any] = {}
    for pid, product in products.items():
        data['products'][pid] = {
            'product_id': product.product_id,
            'name': product.name,
            'price': product.price,
            'quantity_available': product.quantity_available,
            'category': product.category,
            'weight': product.weight,
            'supplier_id': product.supplier_id
        }

    # Convert customers
    # Note: This code references old global variables that no longer exist
    customers: dict[str, Any] = {}
    for cid, customer in customers.items():
        data['customers'][cid] = {
            'customer_id': customer.customer_id,
            'name': customer.name,
            'email': customer.email,
            'membership_tier': customer.membership_tier,
            'phone': customer.phone,
            'address': customer.address,
            'loyalty_points': customer.loyalty_points,
            'order_history': customer.order_history
        }

    # Convert orders (simplified)
    # Note: This code references old global variables that no longer exist
    orders: dict[str, Any] = {}
    for oid, order in orders.items():
        data['orders'][oid] = {
            'order_id': order.order_id,
            'customer_id': order.customer_id,
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'total_price': order.total_price
        }

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Data saved to {filename}")

def load_data_from_file(filename: str) -> bool:
    # Load data (also monolithic)
    # Note: This code references old functions that no longer exist
    # This file needs refactoring to use OrderProcessor
    try:
        with open(filename, 'r') as f:
            data: dict[str, Any] = json.load(f)

        # Load products
        # Note: add_product function from old order_system no longer exists
        add_product: Any = None
        for pid, pdata in data.get('products', {}).items():
            if add_product is not None:
                add_product(
                    pdata['product_id'],
                    pdata['name'],
                    pdata['price'],
                    pdata['quantity_available'],
                    pdata['category'],
                    pdata['weight'],
                    pdata['supplier_id']
                )

        # Load customers
        # Note: add_customer function from old order_system no longer exists
        add_customer: Any = None
        customers: dict[str, Any] = {}
        for cid, cdata in data.get('customers', {}).items():
            if add_customer is not None:
                add_customer(
                    cdata['customer_id'],
                    cdata['name'],
                    cdata['email'],
                    cdata['membership_tier'],
                    cdata['phone'],
                    cdata['address']
                )
                customer = customers.get(cdata['customer_id'])
                if customer is not None:
                    customer.loyalty_points = cdata['loyalty_points']
                    customer.order_history = cdata['order_history']

        print(f"Data loaded from {filename}")
        return True
    except FileNotFoundError:
        print(f"File {filename} not found")
        return False
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

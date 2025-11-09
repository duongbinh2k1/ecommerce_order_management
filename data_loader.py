"""
Data Loader Service - Handles data persistence and loading.
Refactored to work with the new OrderProcessor architecture.

This service provides functionality to:
- Save system state to JSON files
- Load system state from JSON files
- Export/Import data for backup and migration

Follows Single Responsibility Principle - only handles data serialization.
"""
import json
import datetime
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from application.order_processor import OrderProcessor


class DataLoaderService:
    """Service for data persistence and loading operations."""

    def __init__(self, order_processor: 'OrderProcessor') -> None:
        """
        Initialize data loader with OrderProcessor dependency.
        
        Args:
            order_processor: Application orchestrator for accessing all services
        """
        self.__order_processor = order_processor

    def save_data_to_file(self, filename: str) -> bool:
        """
        Save all system data to a JSON file.

        Args:
            filename: Target filename for saving data

        Returns:
            True if successful, False otherwise
        """
        try:
            data: dict[str, Any] = {
                'products': {},
                'customers': {},
                'orders': {},
                'suppliers': {},
                'promotions': {},
                'metadata': {
                    'exported_at': datetime.datetime.now().isoformat(),
                    'version': '1.0'
                }
            }

            # Convert products using ProductService
            products = self.__order_processor.product_service.get_all_products()
            for pid, product in products.items():
                data['products'][str(pid)] = {
                    'product_id': product.product_id,
                    'name': product.name,
                    'price': product.price.value,  # Extract Money value
                    'quantity_available': product.quantity_available,
                    'category': product.category,
                    'weight': product.weight,
                    'supplier_id': product.supplier_id
                }

            # Convert customers using CustomerService
            customers = self.__order_processor.customer_service.get_all_customers()
            for cid, customer in customers.items():
                data['customers'][str(cid)] = {
                    'customer_id': customer.customer_id,
                    'name': customer.name,
                    'email': customer.email.value,  # Extract Email value
                    'membership_tier': customer.membership_tier.value,  # Extract enum value
                    'phone': customer.phone.value if customer.phone.value else "",
                    'address': customer.address.value,  # Extract Address value
                    'loyalty_points': customer.loyalty_points,
                    'order_history': customer.order_history
                }

            # Convert orders using OrderService
            orders = self.__order_processor.order_service.get_all_orders()
            for oid, order in orders.items():
                # Convert order items
                items_data = []
                for item in order.items:
                    items_data.append({
                        'product_id': item.product_id,
                        'quantity': item.quantity,
                        'unit_price': item.unit_price.value,  # Extract Money value
                        'discount_applied': item.discount_applied
                    })

                data['orders'][str(oid)] = {
                    'order_id': order.order_id,
                    'customer_id': order.customer_id,
                    'status': order.status.value,  # Extract enum value
                    'created_at': order.created_at.isoformat(),
                    'total_price': order.total_price.value,  # Extract Money value
                    'shipping_cost': order.shipping_cost.value,  # Extract Money value
                    'items': items_data,
                    'tracking_number': order.tracking_number
                }

            # Save to file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

            print(f"✓ Data saved to {filename}")
            return True

        except (IOError, ValueError, TypeError) as e:
            print(f"✗ Error saving data: {e}")
            return False

    def load_data_from_file(self, filename: str) -> bool:
        """
        Load system data from a JSON file.

        Args:
            filename: Source filename to load data from

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data: dict[str, Any] = json.load(f)

            print(f"Loading data from {filename}...")

            # Load suppliers first (products depend on suppliers)
            suppliers_data = data.get('suppliers', {})
            for sdata in suppliers_data.values():
                self.__order_processor.add_supplier(
                    supplier_id=sdata['supplier_id'],
                    name=sdata['name'],
                    email=sdata['email'],
                    reliability=sdata['reliability_score']
                )

            # Load products
            products_data = data.get('products', {})
            for pdata in products_data.values():
                self.__order_processor.add_product(
                    product_id=pdata['product_id'],
                    name=pdata['name'],
                    price=pdata['price'],
                    quantity=pdata['quantity_available'],
                    category=pdata['category'],
                    weight=pdata['weight'],
                    supplier_id=pdata['supplier_id']
                )

            # Load customers
            customers_data = data.get('customers', {})
            for cdata in customers_data.values():
                self.__order_processor.add_customer(
                    customer_id=cdata['customer_id'],
                    name=cdata['name'],
                    email=cdata['email'],
                    tier=cdata['membership_tier'],
                    phone=cdata['phone'],
                    address=cdata['address']
                )

                # Update loyalty points and order history manually
                customer = self.__order_processor.customer_service.get_customer(cdata['customer_id'])
                if customer:
                    # Add loyalty points
                    points_to_add = cdata['loyalty_points'] - customer.loyalty_points
                    if points_to_add > 0:
                        self.__order_processor.customer_service.add_loyalty_points(
                            cdata['customer_id'], points_to_add)

            # Load promotions
            promotions_data = data.get('promotions', {})
            for pdata in promotions_data.values():
                # Convert ISO string back to datetime
                valid_until = datetime.datetime.fromisoformat(pdata['valid_until'])
                self.__order_processor.add_promotion(
                    promo_id=pdata['promo_id'],
                    code=pdata['code'],
                    discount=pdata['discount_percent'],
                    min_purchase=pdata['min_purchase'],
                    valid_until=valid_until,
                    category=pdata['category']
                )

            # Note: Orders are not loaded as they require complex reconstruction
            # In a real system, you might want to recreate orders or store them separately

            metadata = data.get('metadata', {})
            exported_at = metadata.get('exported_at', 'unknown')
            print(f"✓ Data loaded from {filename} (exported at: {exported_at})")
            return True

        except FileNotFoundError:
            print(f"✗ File {filename} not found")
            return False
        except (IOError, ValueError, TypeError, KeyError) as e:
            print(f"✗ Error loading data: {e}")
            return False

    def export_customers_csv(self, filename: str) -> bool:
        """
        Export customers to CSV format.

        Args:
            filename: Target CSV filename

        Returns:
            True if successful, False otherwise
        """
        try:
            import csv

            customers = self.__order_processor.customer_service.get_all_customers()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'customer_id', 'name', 'email', 'membership_tier',
                    'phone', 'address', 'loyalty_points', 'total_orders'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for customer in customers.values():
                    writer.writerow({
                        'customer_id': customer.customer_id,
                        'name': customer.name,
                        'email': customer.email.value,
                        'membership_tier': customer.membership_tier.value,
                        'phone': customer.phone.value if customer.phone.value else "",
                        'address': customer.address.value,
                        'loyalty_points': customer.loyalty_points,
                        'total_orders': len(customer.order_history)
                    })

            print(f"✓ Customers exported to {filename}")
            return True

        except (IOError, ImportError, AttributeError) as e:
            print(f"✗ Error exporting customers: {e}")
            return False

    def get_data_summary(self) -> dict[str, int]:
        """
        Get a summary of current system data.

        Returns:
            Dictionary with counts of various entities
        """
        products = self.__order_processor.product_service.get_all_products()
        customers = self.__order_processor.customer_service.get_all_customers()
        orders = self.__order_processor.order_service.get_all_orders()

        return {
            'total_products': len(products),
            'total_customers': len(customers),
            'total_orders': len(orders),
            'low_stock_products': len(self.__order_processor.inventory_service.get_low_stock_products(10))
        }


# Convenience functions for backward compatibility
def save_data_to_file(order_processor: 'OrderProcessor', filename: str) -> bool:
    """
    Convenience function to save data using OrderProcessor.

    Args:
        order_processor: Application orchestrator
        filename: Target filename

    Returns:
        True if successful, False otherwise
    """
    loader = DataLoaderService(order_processor)
    return loader.save_data_to_file(filename)


def load_data_from_file(order_processor: 'OrderProcessor', filename: str) -> bool:
    """
    Convenience function to load data using OrderProcessor.

    Args:
        order_processor: Application orchestrator
        filename: Source filename

    Returns:
        True if successful, False otherwise
    """
    loader = DataLoaderService(order_processor)
    return loader.load_data_from_file(filename)

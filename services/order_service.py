"""Order Service - Handles order creation and management."""

from typing import Optional, TYPE_CHECKING
import datetime
from domain.models.order import Order
from domain.models.order_item import OrderItem
from domain.enums.order_status import OrderStatus
from domain.enums.payment_method import PaymentMethod
from domain.enums.shipping_method import ShippingMethod
from domain.enums.membership_tier import MembershipTier
from repositories.interfaces.order_repository import OrderRepository

if TYPE_CHECKING:
    from services.product_service import ProductService
    from services.customer_service import CustomerService
    from services.pricing.pricing_service import PricingService
    from services.payment_service import PaymentService
    from services.shipping_service import ShippingService
    from services.notification_service import NotificationService
    from services.inventory_service import InventoryService


class OrderService:
    """Service for order management operations (orchestrates other services)."""

    def __init__(
        self,
        order_repository: OrderRepository,
        product_service: 'ProductService',
        customer_service: 'CustomerService',
        pricing_service: 'PricingService',
        payment_service: 'PaymentService',
        shipping_service: 'ShippingService',
        notification_service: 'NotificationService',
        inventory_service: 'InventoryService'
    ) -> None:
        """
        Initialize the order service with dependencies (Dependency Injection).
        
        Args:
            order_repository: Repository for order data access
            product_service, customer_service, etc.: Injected service dependencies
        """
        self.__repository = order_repository
        self.__product_service = product_service
        self.__customer_service = customer_service
        self.__pricing_service = pricing_service
        self.__payment_service = payment_service
        self.__shipping_service = shipping_service
        self.__notification_service = notification_service
        self.__inventory_service = inventory_service

    def create_order(
        self,
        customer_id: int,
        # (product_id, quantity, unit_price)
        order_items: list[tuple[int, int, float]],
        payment_info: dict,
        promo_code: Optional[str] = None,
        shipping_method: str = 'standard'
    ) -> Optional[Order]:
        """
        Create a new order (this is the giant process_order refactored).

        Args:
            customer_id: Customer placing the order
            order_items: List of (product_id, quantity, unit_price) tuples
            payment_info: Payment information dictionary
            promo_code: Optional promotion code
            shipping_method: Shipping method

        Returns:
            Order object if successful, None otherwise
        """
        # Step 1: Validate customer
        customer = self.__customer_service.get_customer(customer_id)
        if not customer:
            print("Customer not found")
            return None

        if customer.membership_tier == MembershipTier.SUSPENDED:
            print("Customer account is suspended")
            return None

        # Step 2: Validate products and stock availability
        order_item_objects = []
        products = {}

        for product_id, quantity, unit_price in order_items:
            product = self.__product_service.get_product(product_id)
            if not product:
                print(f"Product {product_id} not found")
                return None

            if not self.__inventory_service.check_product_availability(product_id, quantity):
                print(f"Not enough stock for {product.name}")
                return None

            # Create OrderItem
            order_item = OrderItem(
                product_id=product_id,
                quantity=quantity,
                unit_price=unit_price
            )
            order_item_objects.append(order_item)
            products[product_id] = product

        # Step 3: Calculate pricing with all discounts
        # TODO: Add PromotionService to get promotion by code
        promotion = None

        pricing_breakdown = self.__pricing_service.apply_all_discounts(
            customer=customer,
            order_items=order_item_objects,
            products=products,
            promotion=promotion
        )

        # Step 4: Calculate shipping cost
        shipping_method_enum = ShippingMethod(shipping_method)
        shipping_cost = self.__shipping_service.calculate_shipping_cost(
            shipping_method=shipping_method_enum,
            total_weight=pricing_breakdown['total_weight'],
            subtotal=pricing_breakdown['final_price'],
            customer_tier=customer.membership_tier
        )

        # Step 5: Calculate tax
        tax = self.__calculate_tax(
            subtotal=pricing_breakdown['final_price'],
            customer_address=customer.address.value
        )

        # Step 6: Calculate final total
        total_price = pricing_breakdown['final_price'] + shipping_cost + tax

        # Step 7: Validate and process payment
        payment_method_enum = PaymentMethod(
            payment_info.get('type', 'credit_card'))
        order_id = self.__repository.get_next_id()

        is_valid, error = self.__payment_service.process_payment(
            order_id=str(order_id),
            amount=total_price,
            payment_method=payment_method_enum,
            payment_info=payment_info
        )

        if not is_valid:
            print(f"Payment failed: {error}")
            return None

        # Step 8: Deduct inventory
        for product_id, quantity, _ in order_items:
            product = products[product_id]
            new_quantity = product.quantity_available - quantity
            self.__product_service.update_product_quantity(
                product_id, new_quantity)
            self.__inventory_service.log_inventory_change(
                product_id, -quantity, "sale")

        # Step 9: Create Order object
        order = Order(
            order_id=order_id,
            customer_id=customer_id,
            items=order_item_objects,
            total_price=total_price,
            status='pending',
            created_at=datetime.datetime.now(),
            shipping_cost=shipping_cost
        )

        self.__repository.add(order)

        # Step 10: Update customer order history and loyalty points
        self.__customer_service.add_order_to_history(customer_id, order_id)
        points_earned = int(total_price * 0.1)  # 10% of total as points
        self.__customer_service.add_loyalty_points(customer_id, points_earned)

        # Step 11: Send confirmation notification
        self.__notification_service.send_order_confirmation(customer, order)

        print(
            f"Order {order_id} created successfully! Total: ${total_price:.2f}")
        return order

    def __calculate_tax(self, subtotal: float, customer_address: str) -> float:
        """
        Calculate tax based on customer address.

        Args:
            subtotal: Order subtotal
            customer_address: Customer address

        Returns:
            Tax amount
        """
        tax_rate = 0.08  # Default
        if 'CA' in customer_address:
            tax_rate = 0.0725
        elif 'NY' in customer_address:
            tax_rate = 0.04
        elif 'TX' in customer_address:
            tax_rate = 0.0625

        return subtotal * tax_rate

    def get_order(self, order_id: str) -> Optional[Order]:
        """Get an order by ID."""
        return self.__repository.get(order_id)

    def cancel_order(self, order_id: str, reason: str) -> bool:
        """
        Cancel an order and refund payment.

        Args:
            order_id: Order identifier
            reason: Cancellation reason

        Returns:
            True if successful
        """
        order = self.__repository.get(order_id)
        if not order:
            print("Order not found")
            return False

        if order.status != OrderStatus.PENDING:
            print("Can only cancel pending orders")
            return False

        # Restore inventory
        products = self.__product_service.get_all_products()
        for item in order.order_items:
            product = products.get(item.product_id)
            if product:
                new_quantity = product.quantity_available + item.quantity
                self.__product_service.update_product_quantity(
                    item.product_id, new_quantity)
                self.__inventory_service.log_inventory_change(
                    item.product_id,
                    item.quantity,
                    f"order_cancelled_{order_id}"
                )

        # Process refund
        self.__payment_service.process_refund(
            order_id=order_id,
            amount=order.total_price.value,
            reason=reason
        )

        # Note: Order is immutable, would need to recreate or add setter
        print(f"Order {order_id} cancelled: {reason}")
        return True

    def ship_order(self, order_id: str) -> Optional[str]:
        """
        Ship an order and generate tracking number.

        Args:
            order_id: Order identifier

        Returns:
            Tracking number or None if failed
        """
        order = self.__repository.get(order_id)
        if not order:
            print("Order not found")
            return None

        customer = self.__customer_service.get_customer(order.customer_id)
        if not customer:
            return None

        # Create shipment
        tracking_number = self.__shipping_service.create_shipment(
            order_id=order_id,
            shipping_method='standard',  # TODO: Add shipping_method to Order model
            address=customer.address.value
        )

        # Send notification
        self.__notification_service.send_shipment_notification(
            customer=customer,
            order_id=order_id,
            tracking_number=tracking_number
        )

        # Note: Order status would need to be updated via setter or recreation
        print(f"Order {order_id} shipped! Tracking: {tracking_number}")
        return tracking_number

    def get_customer_orders(self, customer_id: str) -> list[Order]:
        """
        Get all orders for a customer.

        Args:
            customer_id: Customer identifier

        Returns:
            List of orders
        """
        customer = self.__customer_service.get_customer(customer_id)
        if not customer:
            return []

        return [
            self.__repository.get(str(order_id))
            for order_id in customer.order_history
            if self.__repository.exists(str(order_id))
        ]

    def get_all_orders(self) -> dict[str, Order]:
        """Get all orders."""
        return self.__repository.get_all()

    def update_order_status(
        self,
        order_id: str,
        new_status: str
    ) -> Optional[Order]:
        """
        Update order status and send notifications.

        Args:
            order_id: Order identifier
            new_status: New status value

        Returns:
            Updated order or None if failed
        """
        order = self.__repository.get(order_id)
        if not order:
            return None

        # Note: Order is immutable, would need recreation with new status
        # For now, just handle notifications
        customer = self.__customer_service.get_customer(str(order.customer_id))
        if customer:
            print(
                f"To: {customer.email.value}: Order {order_id} status changed to {new_status}")

        # If shipped, create tracking
        if new_status == 'shipped':
            tracking_number = self.ship_order(order_id)
            if tracking_number:
                print(f"Shipment created with tracking: {tracking_number}")

        return order

    def apply_additional_discount(
        self,
        order_id: str,
        discount_percent: float,
        reason: str
    ) -> Optional[Order]:
        """
        Apply additional manual discount to pending order.

        Args:
            order_id: Order identifier
            discount_percent: Discount percentage (0-100)
            reason: Reason for discount

        Returns:
            Updated order or None if failed
        """
        order = self.__repository.get(order_id)
        if not order:
            return None

        if order.status != OrderStatus.PENDING:
            print("Can only apply discount to pending orders")
            return None

        new_price = self.__pricing_service.calculate_additional_discount(
            current_price=order.total_price.value,
            discount_percent=discount_percent
        )

        print(
            f"Applied {discount_percent}% discount to order {order_id}. Reason: {reason}")
        print(
            f"New total: ${new_price:.2f} (was ${order.total_price.value:.2f})")

        # Would need to recreate order with new price (immutability)
        return order

"""Order Service - Handles order creation and management."""

from typing import Any, Optional, TYPE_CHECKING
import datetime
from domain.models.order import Order
from domain.models.order_item import OrderItem
from domain.enums.order_status import OrderStatus
from domain.enums.payment_method import PaymentMethod
from domain.enums.shipping_method import ShippingMethod
from domain.enums.membership_tier import MembershipTier
from domain.enums.us_state import USState
from repositories.interfaces.order_repository import OrderRepository

if TYPE_CHECKING:
    from services.product_service import ProductService
    from services.customer_service import CustomerService
    from services.pricing.pricing_service import PricingService
    from services.payment_service import PaymentService
    from services.shipping_service import ShippingService
    from services.shipment_service import ShipmentService
    from services.notification_service import NotificationService
    from services.inventory_service import InventoryService
    from services.promotion_service import PromotionService
    from services.supplier_service import SupplierService


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
        shipment_service: 'ShipmentService',
        notification_service: 'NotificationService',
        inventory_service: 'InventoryService',
        supplier_service: 'SupplierService',
        promotion_service: Optional['PromotionService'] = None
    ) -> None:
        """
        Initialize the order service with dependencies (Dependency Injection).
        
        Args:
            order_repository: Repository for order data access
            product_service, customer_service, etc.: Injected service dependencies
            supplier_service: Service for supplier operations
        """
        self.__repository = order_repository
        self.__product_service = product_service
        self.__customer_service = customer_service
        self.__pricing_service = pricing_service
        self.__payment_service = payment_service
        self.__shipping_service = shipping_service
        self.__shipment_service = shipment_service
        self.__notification_service = notification_service
        self.__inventory_service = inventory_service
        self.__supplier_service = supplier_service
        self.__promotion_service = promotion_service

    def create_order(
        self,
        customer_id: int,
        # (product_id, quantity, unit_price)
        order_items: list[tuple[int, int, float]],
        payment_info: dict[str, Any],
        promo_code: Optional[str] = None,
        shipping_method: ShippingMethod = ShippingMethod.STANDARD
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
        # Get promotion from promo_code using PromotionService
        promotion = None
        if promo_code and self.__promotion_service:
            promotion = self.__promotion_service.get_promotion(promo_code)
            if promotion:
                # Increment usage count
                self.__promotion_service.increment_usage(promo_code)

        pricing_breakdown = self.__pricing_service.apply_all_discounts(
            customer=customer,
            order_items=order_item_objects,
            products=products,
            promotion=promotion
        )

        # Step 4: Calculate shipping cost
        shipping_cost = self.__shipping_service.calculate_shipping_cost(
            shipping_method=shipping_method,
            total_weight=pricing_breakdown.total_weight,
            subtotal=pricing_breakdown.subtotal_after_loyalty.value,
            customer_tier=customer.membership_tier
        )

        # Step 5: Calculate tax
        tax = self.__calculate_tax(
            subtotal=pricing_breakdown.subtotal_after_loyalty.value,
            customer_address=customer.address.value
        )

        # Step 6: Calculate final total 
        base_amount = pricing_breakdown.subtotal_after_loyalty.value
        total_price = base_amount + shipping_cost + tax

        # Step 7: Validate and process payment
        payment_method_enum = PaymentMethod(
            payment_info.get('type', PaymentMethod.CREDIT_CARD))
        order_id = self.__repository.get_next_id()

        is_valid, error = self.__payment_service.process_payment(
            order_id=order_id,
            amount=total_price,
            payment_method=payment_method_enum,
            payment_info=payment_info
        )

        if not is_valid:
            print(f"Payment failed: {error}")
            return None

        # Step 7.5: Deduct loyalty points (like legacy system)
        if pricing_breakdown.loyalty_points_used > 0:
            new_loyalty_points = customer.loyalty_points - pricing_breakdown.loyalty_points_used
            self.__customer_service.update_loyalty_points(customer_id, new_loyalty_points)

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
            status=OrderStatus.PENDING,
            created_at=datetime.datetime.now(),
            shipping_cost=shipping_cost
        )

        self.__repository.add(order)

        # Step 10: Update customer order history and loyalty points
        self.__customer_service.add_order_to_history(customer_id, order_id)
        # Award loyalty points like legacy: 1 point per dollar of ORIGINAL subtotal (before discounts)
        points_earned = int(pricing_breakdown.original_subtotal.value)  # Match legacy: int(subtotal)
        self.__customer_service.add_loyalty_points(customer_id, points_earned)

        # Step 11: Send confirmation notification
        self.__notification_service.send_order_confirmation(customer, order)

        # Step 12: Check for low stock and notify suppliers (match legacy system)
        for product_id, quantity, _ in order_items:
            product = products[product_id]
            if product.quantity_available < 5:  # Low stock threshold like legacy
                self.__supplier_service.notify_supplier_reorder(
                    product_id, product.supplier_id)

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
        if USState.CA.value in customer_address:
            tax_rate = 0.0725
        elif USState.NY.value in customer_address:
            tax_rate = 0.04
        elif USState.TX.value in customer_address:
            tax_rate = 0.0625

        return subtotal * tax_rate

    def get_order(self, order_id: int) -> Optional[Order]:
        """Get an order by ID."""
        return self.__repository.get(order_id)

    def cancel_order(self, order_id: int, reason: str) -> bool:
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
        for item in order.items:
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
        
        # Update order status to cancelled (like legacy system)
        order.status = OrderStatus.CANCELLED
        self.__repository.update(order)
        
        # Send cancellation notification like legacy system
        customer = self.__customer_service.get_customer(order.customer_id)
        if customer:
            self.__notification_service.send_order_cancellation(
                customer, order_id, reason)
        
        print(f"Order {order_id} cancelled: {reason}")
        return True

    def ship_order(self, order_id: int) -> Optional[str]:
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
        tracking_number = self.__shipment_service.create_shipment(
            order_id=order_id,
            shipping_method=ShippingMethod.STANDARD,
            address=customer.address.value
        )

        return tracking_number

    def get_customer_orders(self, customer_id: int) -> list[Order]:
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
            order
            for order_id in customer.order_history
            if (order := self.__repository.get(order_id)) is not None
        ]

    def get_all_orders(self) -> dict[int, Order]:
        """Get all orders."""
        return self.__repository.get_all()

    def update_order_status(
        self,
        order_id: int,
        new_status: OrderStatus
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

        # Update order status (like legacy system)
        order.status = new_status
        self.__repository.update(order)

        # Send notification (like legacy system)
        customer = self.__customer_service.get_customer(order.customer_id)
        if customer:
            print(f"To: {customer.email}: Order {order_id} status changed to {new_status.value}")

        # If shipped, create tracking (like legacy system)
        if new_status == OrderStatus.SHIPPED and not order.tracking_number:
            tracking_number = self.ship_order(order_id)
            if tracking_number:
                order.tracking_number = tracking_number
                self.__repository.update(order)

        return order

    def apply_additional_discount(
        self,
        order_id: int,
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

        # Store old price for display
        old_price = order.total_price.value

        # Update order total price (like legacy system)
        order.total_price = new_price  # Setter expects int|float, not Money
        self.__repository.update(order)

        print(
            f"Applied {discount_percent}% discount to order {order_id}. Reason: {reason}")
        print(
            f"New total: ${new_price:.2f} (was ${old_price:.2f})")

        return order

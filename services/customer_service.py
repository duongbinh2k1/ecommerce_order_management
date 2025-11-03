"""Customer Service - Manages customer operations."""

from typing import Optional
from domain.models.customer import Customer
from domain.enums.membership_tier import MembershipTier


class CustomerService:
    """Service for customer management operations."""

    def __init__(self) -> None:
        """Initialize the customer service."""
        self.__customers: dict[str, Customer] = {}

    def add_customer(
        self,
        customer_id: str,
        name: str,
        email: str,
        tier: str,
        phone: str,
        address: str
    ) -> Customer:
        """
        Add a new customer.

        Args:
            customer_id: Unique customer identifier
            name: Customer name
            email: Customer email address
            tier: Membership tier
            phone: Phone number
            address: Address

        Returns:
            The created Customer instance
        """
        customer = Customer(
            customer_id=customer_id,
            name=name,
            email=email,
            membership_tier=tier,
            phone=phone,
            address=address,
            loyalty_points=0
        )
        self.__customers[customer_id] = customer
        return customer

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """
        Retrieve a customer by ID.

        Args:
            customer_id: The customer identifier

        Returns:
            The Customer if found, None otherwise
        """
        return self.__customers.get(customer_id)

    def add_loyalty_points(self, customer_id: str, points: int) -> bool:
        """
        Add loyalty points to a customer.

        Args:
            customer_id: The customer identifier
            points: Points to add

        Returns:
            True if successful, False if customer not found
        """
        customer = self.__customers.get(customer_id)
        if not customer:
            return False

        # Create updated customer
        new_loyalty_points = customer.loyalty_points + points
        self.__customers[customer_id] = Customer(
            customer_id=customer.customer_id,
            name=customer.name,
            email=customer.email.value,  # Extract primitive
            membership_tier=customer.membership_tier.value,  # Extract primitive
            phone=customer.phone.value if customer.phone else "",
            address=customer.address.value,  # Extract primitive
            loyalty_points=new_loyalty_points
        )
        return True

    def upgrade_membership(
        self,
        customer_id: str,
        new_tier: MembershipTier
    ) -> bool:
        """
        Upgrade customer membership tier.

        Args:
            customer_id: The customer identifier
            new_tier: The new membership tier

        Returns:
            True if successful, False if customer not found
        """
        customer = self.__customers.get(customer_id)
        if not customer:
            return False

        # Create updated customer
        self.__customers[customer_id] = Customer(
            customer_id=customer.customer_id,
            name=customer.name,
            email=customer.email.value,
            membership_tier=new_tier.value,
            phone=customer.phone.value if customer.phone else "",
            address=customer.address.value,
            loyalty_points=customer.loyalty_points
        )
        print(f"Customer {customer.name} upgraded to {new_tier.value}!")
        return True

    def add_order_to_history(self, customer_id: str, order_id: str) -> bool:
        """
        Add an order to customer's order history.

        Args:
            customer_id: The customer identifier
            order_id: The order identifier

        Returns:
            True if successful, False if customer not found
        """
        customer = self.__customers.get(customer_id)
        if not customer:
            return False

        # Add order to history (customer has order_history list)
        customer.order_history.append(order_id)
        return True

    def get_all_customers(self) -> dict[str, Customer]:
        """
        Get all customers.

        Returns:
            Dictionary of all customers
        """
        return self.__customers.copy()

    def auto_upgrade_membership(
        self,
        customer_id: str,
        lifetime_value: float
    ) -> bool:
        """
        Automatically upgrade customer membership based on lifetime value.

        Args:
            customer_id: Customer identifier
            lifetime_value: Customer's lifetime value

        Returns:
            True if upgraded, False otherwise
        """
        customer = self.__customers.get(customer_id)
        if not customer:
            return False

        current_tier = customer.membership_tier
        new_tier = None

        # Upgrade rules based on lifetime value
        if lifetime_value >= 1000 and current_tier != MembershipTier.GOLD:
            new_tier = MembershipTier.GOLD
        elif lifetime_value >= 500 and current_tier == MembershipTier.STANDARD:
            new_tier = MembershipTier.SILVER
        elif lifetime_value >= 200 and current_tier == MembershipTier.STANDARD:
            new_tier = MembershipTier.BRONZE

        if new_tier:
            return self.upgrade_membership(customer_id, new_tier)

        return False

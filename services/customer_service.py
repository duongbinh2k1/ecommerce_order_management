"""Customer Service - Manages customer operations."""

from typing import Optional
from domain.models.customer import Customer
from domain.enums.membership_tier import MembershipTier
from repositories.interfaces.customer_repository import CustomerRepository


class CustomerService:
    """Service for customer management operations."""

    def __init__(self, customer_repository: CustomerRepository) -> None:
        """
        Initialize the customer service.
        
        Args:
            customer_repository: Repository for customer data access (DI)
        """
        self.__repository = customer_repository

    def add_customer(
        self,
        customer_id: int,
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
        self.__repository.add(customer)
        return customer

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """
        Retrieve a customer by ID.

        Args:
            customer_id: The customer identifier

        Returns:
            The Customer if found, None otherwise
        """
        return self.__repository.get(customer_id)

    def add_loyalty_points(self, customer_id: int, points: int) -> bool:
        """
        Add loyalty points to a customer.

        Args:
            customer_id: The customer identifier
            points: Points to add

        Returns:
            True if successful, False if customer not found
        """
        customer = self.__repository.get(customer_id)
        if not customer:
            return False

        # Create updated customer
        new_loyalty_points = customer.loyalty_points + points
        updated_customer = Customer(
            customer_id=customer.customer_id,
            name=customer.name,
            email=customer.email.value,
            membership_tier=customer.membership_tier,
            phone=customer.phone.value if customer.phone.value is not None else "",
            address=customer.address.value,
            loyalty_points=new_loyalty_points,
            order_history=customer.order_history
        )
        self.__repository.update(updated_customer)
        return True

    def upgrade_membership(
        self,
        customer_id: int,
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
        customer = self.__repository.get(customer_id)
        if not customer:
            return False

        # Create updated customer
        updated_customer = Customer(
            customer_id=customer.customer_id,
            name=customer.name,
            email=customer.email.value,
            membership_tier=new_tier,
            phone=customer.phone.value if customer.phone.value is not None else "",
            address=customer.address.value,
            loyalty_points=customer.loyalty_points,
            order_history=customer.order_history
        )
        self.__repository.update(updated_customer)
        print(f"Customer {customer.name} upgraded to {new_tier}!")
        return True

    def add_order_to_history(self, customer_id: int, order_id: int) -> bool:
        """
        Add an order to customer's order history.

        Args:
            customer_id: The customer identifier
            order_id: The order identifier

        Returns:
            True if successful, False if customer not found
        """
        customer = self.__repository.get(customer_id)
        if not customer:
            return False

        # Add order to history (customer has order_history list)
        customer.order_history.append(order_id)
        
        # Create updated customer and save back to repository
        updated_customer = Customer(
            customer_id=customer.customer_id,
            name=customer.name,
            email=customer.email.value,
            membership_tier=customer.membership_tier,
            phone=customer.phone.value if customer.phone.value is not None else "",
            address=customer.address.value,
            loyalty_points=customer.loyalty_points,
            order_history=customer.order_history
        )
        self.__repository.update(updated_customer)
        return True

    def get_all_customers(self) -> dict[int, Customer]:
        """
        Get all customers.

        Returns:
            Dictionary of all customers
        """
        return self.__repository.get_all()

    def auto_upgrade_membership(
        self,
        customer_id: int,
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
        customer = self.__repository.get(customer_id)
        if not customer:
            return False

        current_tier = customer.membership_tier
        new_tier = None

        # Upgrade rules based on lifetime value
        if lifetime_value >= 1000 and current_tier != MembershipTier.GOLD:
            new_tier = MembershipTier.GOLD
            print(f"Customer {customer.name} upgraded to Gold!")
        elif lifetime_value >= 500 and current_tier == MembershipTier.STANDARD:
            new_tier = MembershipTier.SILVER
            print(f"Customer {customer.name} upgraded to Silver!")
        elif lifetime_value >= 200 and current_tier == MembershipTier.STANDARD:
            new_tier = MembershipTier.BRONZE
            print(f"Customer {customer.name} upgraded to Bronze!")

        if new_tier:
            return self.upgrade_membership(customer_id, new_tier)

        return False

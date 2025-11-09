"""
Payment Transaction value object - immutable payment history record
Used by: PaymentService for payment record management
"""
import datetime
from typing import Optional, Any
from domain.value_objects.money import Money
from domain.enums.payment_method import PaymentMethod
from domain.enums.payment_status import PaymentStatus


class PaymentTransaction:
    """Value object representing a payment transaction record."""
    
    def __init__(
        self,
        order_id: int,
        amount: float,
        payment_method: str,
        status: str,
        created_at: Optional[datetime.datetime] = None
    ) -> None:
        """
        Initialize payment transaction.

        Args:
            order_id: Associated order ID
            amount: Payment amount
            payment_method: Payment method (raw value)
            status: Transaction status (raw value)
            created_at: Transaction timestamp (defaults to now)
        """
        self.__validate(order_id, amount)

        self.__order_id = order_id
        self.__amount = Money(amount)
        self.__payment_method = PaymentMethod(payment_method)
        self.__status = PaymentStatus(status)
        self.__created_at = created_at or datetime.datetime.now()

    def __validate(
        self,
        order_id: int,
        amount: float
    ) -> None:
        """Validate transaction data."""
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("Order ID must be a positive integer")
        
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number")

    @property
    def order_id(self) -> int:
        """Get order ID."""
        return self.__order_id

    @property
    def amount(self) -> Money:
        """Get transaction amount."""
        return self.__amount

    @property
    def payment_method(self) -> PaymentMethod:
        """Get payment method."""
        return self.__payment_method

    @property
    def status(self) -> PaymentStatus:
        """Get transaction status."""
        return self.__status

    @property
    def created_at(self) -> datetime.datetime:
        """Get creation timestamp."""
        return self.__created_at

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary for backward compatibility.
        
        Returns:
            dict: Transaction data as dictionary
        """
        return {
            "order_id": self.__order_id,
            "amount": self.__amount.value,
            "payment_method": self.__payment_method,
            "status": self.__status,
            "created_at": self.__created_at
        }

    def __str__(self) -> str:
        """String representation of payment transaction."""
        return f"Payment ${self.__amount.value} for order {self.__order_id} via {self.__payment_method.value}"

    def __repr__(self) -> str:
        """Detailed representation of payment transaction."""
        return (
            f"PaymentTransaction("
            f"order_id={self.__order_id}, "
            f"amount={self.__amount.value}, "
            f"payment_method={self.__payment_method}, "
            f"status={self.__status}, "
            f"created_at={self.__created_at})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality with another payment transaction."""
        if not isinstance(other, PaymentTransaction):
            return False
        
        return (
            self.__order_id == other.order_id and
            self.__amount == other.amount and
            self.__payment_method == other.payment_method and
            self.__status == other.status and
            self.__created_at == other.created_at
        )

    def __hash__(self) -> int:
        """Hash for using in sets/dicts."""
        return hash((
            self.__order_id,
            self.__amount,
            self.__payment_method,
            self.__status,
            self.__created_at
        ))
"""
Payment Transaction domain model - for payment history and refund tracking
Used by: PaymentService for payment record management
"""
import datetime
from typing import Optional, Any
from domain.value_objects.money import Money
from domain.enums.payment_method import PaymentMethod
from domain.enums.payment_status import PaymentStatus


class PaymentTransaction:
    """Domain model representing a payment transaction."""
    
    def __init__(
        self,
        order_id: int,
        amount: float,
        payment_method: PaymentMethod,
        status: PaymentStatus,
        created_at: Optional[datetime.datetime] = None,
        reason: Optional[str] = None
    ) -> None:
        """
        Initialize payment transaction.
        
        Args:
            order_id: Associated order ID
            amount: Payment amount (positive for payments, negative for refunds)
            payment_method: Payment method used
            status: Transaction status
            created_at: Transaction timestamp (defaults to now)
            reason: Optional reason (used for refunds)
        """
        self.__validate(order_id, amount)
        
        self.__order_id = order_id
        self.__amount = Money(abs(amount))  # Store as positive, track sign separately
        self.__is_refund = amount < 0
        self.__payment_method = payment_method
        self.__status = status
        self.__created_at = created_at or datetime.datetime.now()
        self.__reason = reason

    def __validate(
        self,
        order_id: int,
        amount: float
    ) -> None:
        """Validate transaction data."""
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("Order ID must be a positive integer")
        
        if not isinstance(amount, (int, float)) or amount == 0:
            raise ValueError("Amount must be a non-zero number")

    @property
    def order_id(self) -> int:
        """Get order ID."""
        return self.__order_id

    @property
    def amount(self) -> Money:
        """Get transaction amount (always positive)."""
        return self.__amount

    @property
    def signed_amount(self) -> float:
        """Get signed amount (negative for refunds)."""
        return -self.__amount.value if self.__is_refund else self.__amount.value

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

    @property
    def is_refund(self) -> bool:
        """Check if this is a refund transaction."""
        return self.__is_refund

    @property
    def reason(self) -> Optional[str]:
        """Get transaction reason (usually for refunds)."""
        return self.__reason

    def can_be_refunded(self) -> bool:
        """
        Check if this payment can be refunded.
        
        Returns:
            bool: True if payment can be refunded
        """
        if self.__is_refund:
            return False  # Cannot refund a refund
        
        if self.__status != PaymentStatus.COMPLETED:
            return False  # Can only refund completed payments
        
        return True

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary for backward compatibility.
        
        Returns:
            dict: Transaction data as dictionary
        """
        return {
            "order_id": self.__order_id,
            "amount": self.signed_amount,
            "payment_method": self.__payment_method,
            "status": self.__status,
            "created_at": self.__created_at,
            "reason": self.__reason
        }

    def __str__(self) -> str:
        """String representation of payment transaction."""
        amount_str = f"-${self.__amount.value}" if self.__is_refund else f"${self.__amount.value}"
        return f"Payment {amount_str} for order {self.__order_id} via {self.__payment_method.value}"

    def __repr__(self) -> str:
        """Detailed representation of payment transaction."""
        return (
            f"PaymentTransaction("
            f"order_id={self.__order_id}, "
            f"amount={self.signed_amount}, "
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
            self.__is_refund == other.is_refund and
            self.__payment_method == other.payment_method and
            self.__status == other.status and
            self.__created_at == other.created_at and
            self.__reason == other.reason
        )

    def __hash__(self) -> int:
        """Hash for using in sets/dicts."""
        return hash((
            self.__order_id,
            self.__amount,
            self.__is_refund,
            self.__payment_method,
            self.__status,
            self.__created_at,
            self.__reason
        ))
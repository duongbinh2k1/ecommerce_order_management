"""Payment strategy implementations."""

from typing import Protocol, Any
from .credit_card_strategy import CreditCardPaymentStrategy
from .paypal_strategy import PayPalPaymentStrategy


class PaymentStrategy(Protocol):
    """Interface for payment validation strategies."""

    def validate(self, payment_info: dict[str, Any]) -> tuple[bool, str | None]:
        """
        Validate payment information.
        
        Args:
            payment_info: Payment information dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        ...

    def get_payment_type(self) -> str:
        """Return the payment type this strategy handles."""
        ...

__all__ = [
    "PaymentStrategy",
    "CreditCardPaymentStrategy", 
    "PayPalPaymentStrategy",
]
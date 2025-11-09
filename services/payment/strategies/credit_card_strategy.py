"""Credit card payment validation strategy."""

from typing import Any

from domain.enums.payment_method import PaymentMethod


class CreditCardPaymentStrategy:
    """Strategy for validating credit card payments."""
    
    def validate(self, payment_info: dict[str, Any]) -> tuple[bool, str | None]:
        """
        Validate credit card payment information.
        
        Args:
            payment_info: Payment information dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not payment_info.get("valid"):
            return False, "Payment failed - invalid payment info"
        card_number = payment_info.get("card_number", "")
        if len(card_number) < 16:
            return False, "Invalid card number"
        return True, None
    
    def get_payment_type(self) -> str:
        """Return the payment type this strategy handles."""
        return PaymentMethod.CREDIT_CARD
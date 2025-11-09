"""PayPal payment validation strategy."""

from typing import Any

from domain.enums.payment_method import PaymentMethod


class PayPalPaymentStrategy:
    """Strategy for validating PayPal payments."""
    
    def validate(self, payment_info: dict[str, Any]) -> tuple[bool, str | None]:
        """
        Validate PayPal payment information.
        
        Args:
            payment_info: Payment information dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not payment_info.get("valid"):
            return False, "Payment failed - invalid payment info"
        if not payment_info.get("email"):
            return False, "PayPal email required"
        return True, None
    
    def get_payment_type(self) -> str:
        """Return the payment type this strategy handles."""
        return PaymentMethod.PAYPAL
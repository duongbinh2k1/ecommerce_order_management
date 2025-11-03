"""Payment Service - Handles payment validation and processing."""

from typing import Optional
from domain.enums.payment_method import PaymentMethod


class PaymentService:
    """Service for payment validation and processing."""

    def __init__(self) -> None:
        """Initialize the payment service."""
        self.__payment_history: list[dict] = []

    def validate_payment(
        self,
        payment_method: PaymentMethod,
        payment_info: dict
    ) -> tuple[bool, Optional[str]]:
        """
        Validate payment information.

        Args:
            payment_method: Payment method
            payment_info: Payment information dictionary

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Basic validation
        if not payment_info.get("valid"):
            return False, "Payment failed - invalid payment info"

        if payment_method == PaymentMethod.CREDIT_CARD:
            card_number = payment_info.get("card_number", "")
            if len(card_number) < 16:
                return False, "Invalid card number"

        elif payment_method == PaymentMethod.PAYPAL:
            if not payment_info.get("email"):
                return False, "PayPal email required"

        return True, None

    def process_payment(
        self,
        order_id: str,
        amount: float,
        payment_method: PaymentMethod,
        payment_info: dict
    ) -> tuple[bool, Optional[str]]:
        """
        Process payment for an order.

        Args:
            order_id: Order identifier
            amount: Payment amount
            payment_method: Payment method
            payment_info: Payment information

        Returns:
            Tuple of (success, error_message)
        """
        # Validate first
        is_valid, error = self.validate_payment(payment_method, payment_info)
        if not is_valid:
            return False, error

        # Record payment
        self.__payment_history.append({
            'order_id': order_id,
            'amount': amount,
            'payment_method': payment_method.value,
            'status': 'completed'
        })

        return True, None

    def process_refund(
        self,
        order_id: str,
        amount: float,
        reason: str
    ) -> bool:
        """
        Process a refund for an order.

        Args:
            order_id: Order identifier
            amount: Refund amount
            reason: Refund reason

        Returns:
            True if successful
        """
        # Find original payment
        for payment in self.__payment_history:
            if payment['order_id'] == order_id and payment['status'] == 'completed':
                # Record refund
                self.__payment_history.append({
                    'order_id': order_id,
                    'amount': -amount,
                    'payment_method': payment['payment_method'],
                    'status': 'refunded',
                    'reason': reason
                })
                return True

        return False

    def get_payment_history(self, order_id: str) -> list[dict]:
        """
        Get payment history for an order.

        Args:
            order_id: Order identifier

        Returns:
            List of payment records
        """
        return [
            payment for payment in self.__payment_history
            if payment['order_id'] == order_id
        ]

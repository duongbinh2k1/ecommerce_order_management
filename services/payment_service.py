"""Payment Service - Handles payment validation and processing."""

from typing import Optional, Any
from domain.enums.payment_method import PaymentMethod
from domain.enums.payment_status import PaymentStatus
from domain.models.payment_transaction import PaymentTransaction


class PaymentService:
    """Service for processing payments and managing payment history."""
    
    def __init__(self) -> None:
        """Initialize payment service."""
        self.__payment_history: list[PaymentTransaction] = []

    def validate_payment(
        self,
        payment_method: PaymentMethod,
        payment_info: dict[str, Any]
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
        order_id: int,
        amount: float,
        payment_method: PaymentMethod,
        payment_info: dict[str, Any]
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

        # Check payment amount
        provided_amount = payment_info.get("amount", 0)
        if provided_amount < amount:
            return False, "Insufficient payment amount"

        # Record payment transaction
        transaction = PaymentTransaction(
            order_id=order_id,
            amount=amount,
            payment_method=payment_method,
            status=PaymentStatus.COMPLETED
        )
        self.__payment_history.append(transaction)

        return True, None

    def process_refund(
        self,
        order_id: int,
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
        # Find original payment transaction
        original_payment = None
        for transaction in self.__payment_history:
            if (transaction.order_id == order_id and 
                not transaction.is_refund and
                transaction.status == PaymentStatus.COMPLETED):
                original_payment = transaction
                break

        if not original_payment:
            return False

        # Check if refundable
        if not original_payment.can_be_refunded():
            return False

        # Create refund transaction
        refund_transaction = PaymentTransaction(
            order_id=order_id,
            amount=-amount,  # Negative for refund
            payment_method=original_payment.payment_method,
            status=PaymentStatus.REFUNDED,
            reason=reason
        )
        self.__payment_history.append(refund_transaction)

        return True

    def get_payment_history(self, order_id: int) -> list[dict[str, Any]]:
        """
        Get payment history for an order.

        Args:
            order_id: Order identifier

        Returns:
            List of payment records (as dicts for backward compatibility)
        """
        transactions = [
            transaction for transaction in self.__payment_history
            if transaction.order_id == order_id
        ]
        return [transaction.to_dict() for transaction in transactions]

    def get_payment_transactions(self, order_id: int) -> list[PaymentTransaction]:
        """
        Get payment transactions for an order.

        Args:
            order_id: Order identifier

        Returns:
            List of PaymentTransaction objects
        """
        return [
            transaction for transaction in self.__payment_history
            if transaction.order_id == order_id
        ]

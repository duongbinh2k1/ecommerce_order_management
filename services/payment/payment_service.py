"""Payment Service - Handles payment validation and processing using Strategy Pattern."""

from typing import Optional, Any
from domain.enums.payment_method import PaymentMethod
from domain.enums.payment_status import PaymentStatus
from domain.value_objects.payment_transaction import PaymentTransaction
from .strategies import (
    PaymentStrategy,
    CreditCardPaymentStrategy,
    PayPalPaymentStrategy
)


class PaymentService:
    """Service for processing payments and managing payment history using Strategy Pattern."""
    
    def __init__(self, payment_strategies: Optional[list[PaymentStrategy]] = None) -> None:
        """Initialize payment service with injectable strategies."""
        self.__payment_history: list[PaymentTransaction] = []
        self.__strategies: dict[str, PaymentStrategy] = {}
        
        # Register provided strategies or defaults
        strategies = payment_strategies or [
            CreditCardPaymentStrategy(),
            PayPalPaymentStrategy()
        ]
        
        for strategy in strategies:
            self.register_strategy(strategy)
    
    def register_strategy(self, strategy: PaymentStrategy) -> None:
        """
        Register a new payment strategy.
        
        Args:
            strategy: Payment strategy to register
        """
        payment_type = strategy.get_payment_type()
        self.__strategies[payment_type] = strategy

    def validate_payment(
        self,
        payment_method: PaymentMethod,
        payment_info: dict[str, Any]
    ) -> tuple[bool, Optional[str]]:
        """
        Validate payment information using strategy pattern.

        Args:
            payment_method: Payment method enum
            payment_info: Payment information dictionary

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Convert enum to string for strategy lookup
        payment_type = payment_method.value.lower()
        
        strategy = self.__strategies.get(payment_type)
        if not strategy:
            return False, f"Unsupported payment method: {payment_type}"
        
        # Use strategy to validate (no if-else needed!)
        return strategy.validate(payment_info)

    def process_payment(
        self,
        order_id: int,
        amount: float,
        payment_method: PaymentMethod,
        payment_info: dict[str, Any]
    ) -> tuple[bool, Optional[str]]:
        """
        Process payment for an order using strategy pattern.

        Args:
            order_id: Order identifier
            amount: Payment amount
            payment_method: Payment method
            payment_info: Payment information

        Returns:
            Tuple of (success, error_message)
        """
        # Validate using strategy pattern (no if-else!)
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

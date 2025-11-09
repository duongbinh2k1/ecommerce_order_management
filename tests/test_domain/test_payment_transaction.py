"""
Test PaymentTransaction domain model - validation and business rules
Tests payment transaction creation, validation, and business logic
"""
import unittest
import datetime
from domain.models.payment_transaction import PaymentTransaction
from domain.enums.payment_method import PaymentMethod
from domain.enums.payment_status import PaymentStatus
from domain.value_objects.money import Money


class TestPaymentTransaction(unittest.TestCase):
    """Test PaymentTransaction domain model."""

    def test_payment_transaction_creation_valid(self) -> None:
        """Test creating PaymentTransaction with valid data."""
        transaction = PaymentTransaction(
            order_id=123,
            amount=100.0,
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.COMPLETED
        )
        
        self.assertEqual(transaction.order_id, 123)
        self.assertEqual(transaction.amount, Money(100.0))
        self.assertEqual(transaction.signed_amount, 100.0)
        self.assertFalse(transaction.is_refund)
        self.assertEqual(transaction.payment_method, PaymentMethod.CREDIT_CARD)
        self.assertEqual(transaction.status, PaymentStatus.COMPLETED)
        self.assertIsInstance(transaction.created_at, datetime.datetime)

    def test_refund_transaction_creation(self) -> None:
        """Test creating a refund transaction (negative amount)."""
        transaction = PaymentTransaction(
            order_id=123,
            amount=-50.0,  # Negative for refund
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.REFUNDED,
            reason="Customer request"
        )
        
        self.assertEqual(transaction.order_id, 123)
        self.assertEqual(transaction.amount, Money(50.0))  # Stored as positive
        self.assertEqual(transaction.signed_amount, -50.0)  # Negative for refund
        self.assertTrue(transaction.is_refund)
        self.assertEqual(transaction.reason, "Customer request")

    def test_invalid_order_id(self) -> None:
        """Test validation for invalid order ID."""
        with self.assertRaises(ValueError) as context:
            PaymentTransaction(
                order_id=0,  # Invalid
                amount=100.0,
                payment_method=PaymentMethod.CREDIT_CARD,
                status=PaymentStatus.COMPLETED
            )
        self.assertIn("Order ID must be a positive integer", str(context.exception))

    def test_zero_amount(self) -> None:
        """Test validation for zero amount."""
        with self.assertRaises(ValueError) as context:
            PaymentTransaction(
                order_id=123,
                amount=0.0,  # Invalid
                payment_method=PaymentMethod.CREDIT_CARD,
                status=PaymentStatus.COMPLETED
            )
        self.assertIn("Amount must be a non-zero number", str(context.exception))

    def test_can_be_refunded_payment(self) -> None:
        """Test refund eligibility for completed payment."""
        transaction = PaymentTransaction(
            order_id=123,
            amount=100.0,
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.COMPLETED
        )
        
        self.assertTrue(transaction.can_be_refunded())

    def test_cannot_refund_refund(self) -> None:
        """Test that refunds cannot be refunded."""
        transaction = PaymentTransaction(
            order_id=123,
            amount=-50.0,  # Refund
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.REFUNDED
        )
        
        self.assertFalse(transaction.can_be_refunded())

    def test_cannot_refund_pending_payment(self) -> None:
        """Test that pending payments cannot be refunded."""
        transaction = PaymentTransaction(
            order_id=123,
            amount=100.0,
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.PENDING
        )
        
        self.assertFalse(transaction.can_be_refunded())

    def test_to_dict_payment(self) -> None:
        """Test converting payment transaction to dict."""
        transaction = PaymentTransaction(
            order_id=123,
            amount=100.0,
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.COMPLETED,
            reason="Test payment"
        )
        
        result = transaction.to_dict()
        expected = {
            "order_id": 123,
            "amount": 100.0,
            "payment_method": PaymentMethod.CREDIT_CARD,
            "status": PaymentStatus.COMPLETED,
            "created_at": transaction.created_at,
            "reason": "Test payment"
        }
        
        self.assertEqual(result, expected)

    def test_to_dict_refund(self) -> None:
        """Test converting refund transaction to dict."""
        transaction = PaymentTransaction(
            order_id=123,
            amount=-50.0,
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.REFUNDED,
            reason="Customer request"
        )
        
        result = transaction.to_dict()
        
        self.assertEqual(result["amount"], -50.0)  # Should be negative
        self.assertEqual(result["reason"], "Customer request")

    def test_string_representations(self) -> None:
        """Test string representations of transaction."""
        transaction = PaymentTransaction(
            order_id=123,
            amount=100.0,
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.COMPLETED
        )
        
        str_repr = str(transaction)
        self.assertIn("$100.0", str_repr)
        self.assertIn("order 123", str_repr)
        
        repr_str = repr(transaction)
        self.assertIn("PaymentTransaction", repr_str)
        self.assertIn("order_id=123", repr_str)

    def test_equality(self) -> None:
        """Test transaction equality comparison."""
        transaction1 = PaymentTransaction(
            order_id=123,
            amount=100.0,
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.COMPLETED
        )
        
        transaction2 = PaymentTransaction(
            order_id=123,
            amount=100.0,
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.COMPLETED,
            created_at=transaction1.created_at  # Same timestamp
        )
        
        self.assertEqual(transaction1, transaction2)

    def test_inequality_different_amount(self) -> None:
        """Test transaction inequality with different amounts."""
        transaction1 = PaymentTransaction(
            order_id=123,
            amount=100.0,
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.COMPLETED
        )
        
        transaction2 = PaymentTransaction(
            order_id=123,
            amount=200.0,  # Different amount
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.COMPLETED
        )
        
        self.assertNotEqual(transaction1, transaction2)

    def test_custom_created_at(self) -> None:
        """Test transaction with custom creation timestamp."""
        custom_time = datetime.datetime(2024, 1, 15, 10, 30, 0)
        transaction = PaymentTransaction(
            order_id=123,
            amount=100.0,
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.COMPLETED,
            created_at=custom_time
        )
        
        self.assertEqual(transaction.created_at, custom_time)

    def test_hash_functionality(self) -> None:
        """Test that transactions can be used in sets/dicts."""
        transaction = PaymentTransaction(
            order_id=123,
            amount=100.0,
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.COMPLETED
        )
        
        # Should be able to hash (for sets/dicts)
        transaction_set = {transaction}
        self.assertIn(transaction, transaction_set)


if __name__ == '__main__':
    unittest.main()
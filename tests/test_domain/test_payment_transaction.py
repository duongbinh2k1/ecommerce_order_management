"""
Test cases for PaymentTransaction value object.
Tests immutability, validation, and all public methods.
"""
from typing import Any
import unittest
import unittest.mock
import datetime
from unittest.mock import patch
from domain.value_objects.payment_transaction import PaymentTransaction
from domain.value_objects.money import Money
from domain.enums.payment_method import PaymentMethod
from domain.enums.payment_status import PaymentStatus


class TestPaymentTransaction(unittest.TestCase):
    """Test cases for PaymentTransaction value object."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.valid_order_id = 1001
        self.valid_amount = 99.99
        self.valid_payment_method = PaymentMethod.CREDIT_CARD
        self.valid_status = PaymentStatus.COMPLETED
        self.fixed_datetime = datetime.datetime(2024, 1, 15, 10, 30, 0)

    def test_valid_payment_transaction_creation(self) -> None:
        """Test creation of valid payment transaction."""
        transaction = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status
        )

        self.assertEqual(transaction.order_id, self.valid_order_id)
        self.assertEqual(transaction.amount, Money(self.valid_amount))
        self.assertEqual(transaction.payment_method, self.valid_payment_method)
        self.assertEqual(transaction.status, self.valid_status)
        self.assertIsInstance(transaction.created_at, datetime.datetime)

    def test_payment_transaction_with_custom_created_at(self) -> None:
        """Test creation with custom created_at timestamp."""
        custom_time = datetime.datetime(2024, 1, 15, 10, 30, 0)

        transaction = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status,
            created_at=custom_time
        )

        self.assertEqual(transaction.created_at, custom_time)

    @patch('datetime.datetime')
    def test_payment_transaction_default_created_at(self, mock_datetime: unittest.mock.MagicMock) -> None:
        """Test that created_at defaults to current time when not provided."""
        mock_datetime.now.return_value = self.fixed_datetime
        mock_datetime.side_effect = datetime.datetime

        transaction = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status
        )

        mock_datetime.now.assert_called_once()
        self.assertEqual(transaction.created_at, self.fixed_datetime)

    def test_invalid_order_id_validation(self) -> None:
        """Test validation for invalid order IDs."""
        # Test each invalid case individually
        with self.assertRaises(ValueError) as context:
            PaymentTransaction(order_id=0, amount=self.valid_amount,
                               payment_method=self.valid_payment_method, status=self.valid_status)
        self.assertIn("Order ID must be a positive integer",
                      str(context.exception))

        with self.assertRaises(ValueError) as context:
            PaymentTransaction(order_id=-1, amount=self.valid_amount,
                               payment_method=self.valid_payment_method, status=self.valid_status)
        self.assertIn("Order ID must be a positive integer",
                      str(context.exception))

        with self.assertRaises(ValueError) as context:
            PaymentTransaction(order_id=-100, amount=self.valid_amount,
                               payment_method=self.valid_payment_method, status=self.valid_status)
        self.assertIn("Order ID must be a positive integer",
                      str(context.exception))

    def test_invalid_amount_validation(self) -> None:
        """Test validation for invalid amounts."""
        # Test each invalid case individually
        with self.assertRaises(ValueError) as context:
            PaymentTransaction(order_id=self.valid_order_id, amount=0,
                               payment_method=self.valid_payment_method, status=self.valid_status)
        self.assertIn("Amount must be a positive number",
                      str(context.exception))

        with self.assertRaises(ValueError) as context:
            PaymentTransaction(order_id=self.valid_order_id, amount=-1,
                               payment_method=self.valid_payment_method, status=self.valid_status)
        self.assertIn("Amount must be a positive number",
                      str(context.exception))

        with self.assertRaises(ValueError) as context:
            PaymentTransaction(order_id=self.valid_order_id, amount=-0.01,
                               payment_method=self.valid_payment_method, status=self.valid_status)
        self.assertIn("Amount must be a positive number",
                      str(context.exception))

    def test_valid_amount_types(self) -> None:
        """Test that both int and float amounts are accepted."""
        # Test integer amount
        transaction_int = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=100,
            payment_method=self.valid_payment_method,
            status=self.valid_status
        )
        self.assertEqual(transaction_int.amount, Money(100))

        # Test float amount
        transaction_float = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=99.99,
            payment_method=self.valid_payment_method,
            status=self.valid_status
        )
        self.assertEqual(transaction_float.amount, Money(99.99))

    def test_all_payment_methods(self) -> None:
        """Test creation with all available payment methods."""
        for method in PaymentMethod:
            with self.subTest(payment_method=method):
                transaction = PaymentTransaction(
                    order_id=self.valid_order_id,
                    amount=self.valid_amount,
                    payment_method=method,
                    status=self.valid_status
                )
                self.assertEqual(transaction.payment_method, method)

    def test_all_payment_statuses(self) -> None:
        """Test creation with all available payment statuses."""
        for status in PaymentStatus:
            with self.subTest(payment_status=status):
                transaction = PaymentTransaction(
                    order_id=self.valid_order_id,
                    amount=self.valid_amount,
                    payment_method=self.valid_payment_method,
                    status=status
                )
                self.assertEqual(transaction.status, status)

    def test_immutability(self) -> None:
        """Test that PaymentTransaction is immutable."""
        transaction = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status
        )

        # Properties should not have setters - use setattr for proper testing
        with self.assertRaises(AttributeError):
            setattr(transaction, 'order_id', 2000)
        with self.assertRaises(AttributeError):
            setattr(transaction, 'amount', Money(200.0))
        with self.assertRaises(AttributeError):
            setattr(transaction, 'payment_method', PaymentMethod.PAYPAL)
        with self.assertRaises(AttributeError):
            setattr(transaction, 'status', PaymentStatus.FAILED)
        with self.assertRaises(AttributeError):
            setattr(transaction, 'created_at', datetime.datetime.now())

    def test_to_dict_method(self) -> None:
        """Test to_dict conversion method."""
        custom_time = datetime.datetime(2024, 1, 15, 10, 30, 0)
        transaction = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status,
            created_at=custom_time
        )

        expected_dict = {
            "order_id": self.valid_order_id,
            "amount": self.valid_amount,
            "payment_method": self.valid_payment_method,
            "status": self.valid_status,
            "created_at": custom_time
        }

        self.assertEqual(transaction.to_dict(), expected_dict)

    def test_str_method(self) -> None:
        """Test string representation."""
        transaction = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status
        )

        expected_str = f"Payment ${self.valid_amount} for order {self.valid_order_id} via {self.valid_payment_method.value}"
        self.assertEqual(str(transaction), expected_str)

    def test_repr_method(self) -> None:
        """Test detailed representation."""
        custom_time = datetime.datetime(2024, 1, 15, 10, 30, 0)
        transaction = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status,
            created_at=custom_time
        )

        expected_repr = (
            f"PaymentTransaction("
            f"order_id={self.valid_order_id}, "
            f"amount={self.valid_amount}, "
            f"payment_method={self.valid_payment_method}, "
            f"status={self.valid_status}, "
            f"created_at={custom_time})"
        )
        self.assertEqual(repr(transaction), expected_repr)

    def test_equality_same_transactions(self) -> None:
        """Test equality between identical transactions."""
        custom_time = datetime.datetime(2024, 1, 15, 10, 30, 0)

        transaction1 = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status,
            created_at=custom_time
        )

        transaction2 = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status,
            created_at=custom_time
        )

        self.assertEqual(transaction1, transaction2)
        self.assertTrue(transaction1 == transaction2)

    def test_inequality_different_transactions(self) -> None:
        """Test inequality between different transactions."""
        base_transaction = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status,
            created_at=self.fixed_datetime
        )

        # Different order_id
        diff_order = PaymentTransaction(
            order_id=2000,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status,
            created_at=self.fixed_datetime
        )
        self.assertNotEqual(base_transaction, diff_order)

        # Different amount
        diff_amount = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=200.00,
            payment_method=self.valid_payment_method,
            status=self.valid_status,
            created_at=self.fixed_datetime
        )
        self.assertNotEqual(base_transaction, diff_amount)

        # Different payment method
        diff_method = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=PaymentMethod.PAYPAL,
            status=self.valid_status,
            created_at=self.fixed_datetime
        )
        self.assertNotEqual(base_transaction, diff_method)

        # Different status
        diff_status = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=PaymentStatus.FAILED,
            created_at=self.fixed_datetime
        )
        self.assertNotEqual(base_transaction, diff_status)

        # Different created_at
        diff_time = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status,
            created_at=datetime.datetime(2024, 2, 15, 10, 30, 0)
        )
        self.assertNotEqual(base_transaction, diff_time)

    def test_equality_with_non_payment_transaction(self) -> None:
        """Test equality with non-PaymentTransaction objects."""
        transaction = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status
        )

        non_transactions = [
            "not a transaction",
            123,
            {"order_id": self.valid_order_id},
            None,
            []
        ]

        for non_transaction in non_transactions:
            with self.subTest(other=non_transaction):
                self.assertNotEqual(transaction, non_transaction)
                self.assertFalse(transaction == non_transaction)

    def test_hash_consistency(self) -> None:
        """Test that hash is consistent for equal transactions."""
        custom_time = datetime.datetime(2024, 1, 15, 10, 30, 0)

        transaction1 = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status,
            created_at=custom_time
        )

        transaction2 = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status,
            created_at=custom_time
        )

        # Equal objects must have equal hashes
        self.assertEqual(hash(transaction1), hash(transaction2))

    def test_hash_different_for_different_transactions(self) -> None:
        """Test that different transactions have different hashes."""
        transaction1 = PaymentTransaction(
            order_id=1001,
            amount=99.99,
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.COMPLETED,
            created_at=self.fixed_datetime
        )

        transaction2 = PaymentTransaction(
            order_id=1002,
            amount=99.99,
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.COMPLETED,
            created_at=self.fixed_datetime
        )

        # Different transactions should have different hashes (usually)
        self.assertNotEqual(hash(transaction1), hash(transaction2))

    def test_can_be_used_in_set(self) -> None:
        """Test that PaymentTransaction can be used in sets."""
        transaction1 = PaymentTransaction(
            order_id=1001,
            amount=99.99,
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.COMPLETED,
            created_at=self.fixed_datetime
        )

        transaction2 = PaymentTransaction(
            order_id=1002,
            amount=150.00,
            payment_method=PaymentMethod.PAYPAL,
            status=PaymentStatus.PENDING,
            created_at=self.fixed_datetime
        )

        # Should be able to add to set
        transaction_set = {transaction1, transaction2}
        self.assertEqual(len(transaction_set), 2)

        # Adding the same transaction again shouldn't increase size
        transaction_set.add(transaction1)
        self.assertEqual(len(transaction_set), 2)

    def test_can_be_used_as_dict_key(self) -> None:
        """Test that PaymentTransaction can be used as dictionary keys."""
        transaction = PaymentTransaction(
            order_id=self.valid_order_id,
            amount=self.valid_amount,
            payment_method=self.valid_payment_method,
            status=self.valid_status,
            created_at=self.fixed_datetime
        )

        # Should be able to use as dict key
        transaction_dict = {transaction: "processed"}
        self.assertEqual(transaction_dict[transaction], "processed")

    def test_edge_case_amounts(self) -> None:
        """Test edge cases for amount values."""
        edge_amounts = [0.01, 0.1, 1.0, 999999.99]

        for amount in edge_amounts:
            with self.subTest(amount=amount):
                transaction = PaymentTransaction(
                    order_id=self.valid_order_id,
                    amount=amount,
                    payment_method=self.valid_payment_method,
                    status=self.valid_status
                )
                self.assertEqual(transaction.amount, Money(amount))

    def test_edge_case_order_ids(self) -> None:
        """Test edge cases for order ID values."""
        edge_order_ids = [1, 999999]

        for order_id in edge_order_ids:
            with self.subTest(order_id=order_id):
                transaction = PaymentTransaction(
                    order_id=order_id,
                    amount=self.valid_amount,
                    payment_method=self.valid_payment_method,
                    status=self.valid_status
                )
                self.assertEqual(transaction.order_id, order_id)


if __name__ == '__main__':
    unittest.main()
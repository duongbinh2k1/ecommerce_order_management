"""
Test PaymentService - payment processing and validation
Tests payment validation and processing logic
"""
import unittest
from services.payment_service import PaymentService
from domain.enums.payment_method import PaymentMethod


class TestPaymentService(unittest.TestCase):
    """Test PaymentService payment processing."""

    def setUp(self) -> None:
        """Set up test dependencies."""
        self.payment_service = PaymentService()

    def test_validate_payment_valid_credit_card(self) -> None:
        """Test validating valid credit card payment."""
        payment_info = {
            "valid": True,
            "card_number": "1234567890123456"
        }
        
        is_valid, error = self.payment_service.validate_payment(
            PaymentMethod.CREDIT_CARD, payment_info
        )
        
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_payment_invalid_credit_card(self) -> None:
        """Test validating invalid credit card payment."""
        payment_info = {
            "valid": False
        }
        
        is_valid, error = self.payment_service.validate_payment(
            PaymentMethod.CREDIT_CARD, payment_info
        )
        
        self.assertFalse(is_valid)
        self.assertEqual(error, "Payment failed - invalid payment info")

    def test_validate_payment_credit_card_missing_number(self) -> None:
        """Test validating credit card with missing number."""
        payment_info = {
            "valid": True
        }
        
        is_valid, error = self.payment_service.validate_payment(
            PaymentMethod.CREDIT_CARD, payment_info
        )
        
        self.assertFalse(is_valid)
        self.assertEqual(error, "Invalid card number")

    def test_validate_payment_paypal_valid(self) -> None:
        """Test validating valid PayPal payment."""
        payment_info = {
            "valid": True,
            "email": "user@example.com"
        }
        
        is_valid, error = self.payment_service.validate_payment(
            PaymentMethod.PAYPAL, payment_info
        )
        
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_payment_paypal_missing_email(self) -> None:
        """Test validating PayPal with missing email."""
        payment_info = {
            "valid": True
        }
        
        is_valid, error = self.payment_service.validate_payment(
            PaymentMethod.PAYPAL, payment_info
        )
        
        self.assertFalse(is_valid)
        self.assertEqual(error, "PayPal email required")

    def test_process_payment_success(self) -> None:
        """Test successful payment processing."""
        payment_info = {
            "valid": True,
            "card_number": "1234567890123456"
        }
        
        success, error = self.payment_service.process_payment(
            1, 100.0, PaymentMethod.CREDIT_CARD, payment_info
        )
        
        self.assertTrue(success)
        self.assertIsNone(error)

    def test_process_payment_validation_failure(self) -> None:
        """Test payment processing with validation failure."""
        payment_info = {
            "valid": False
        }
        
        success, error = self.payment_service.process_payment(
            2, 100.0, PaymentMethod.CREDIT_CARD, payment_info
        )
        
        self.assertFalse(success)
        self.assertEqual(error, "Payment failed - invalid payment info")

    def test_process_payment_paypal_success(self) -> None:
        """Test successful PayPal payment processing."""
        payment_info = {
            "valid": True,
            "email": "user@example.com"
        }
        
        success, error = self.payment_service.process_payment(
            3, 50.0, PaymentMethod.PAYPAL, payment_info
        )
        
        self.assertTrue(success)
        self.assertIsNone(error)

    def test_get_payment_history(self) -> None:
        """Test getting payment history."""
        # First make a payment
        payment_info = {
            "valid": True,
            "card_number": "1234567890123456"
        }
        
        # Use int order_id consistently
        order_id = 4
        self.payment_service.process_payment(
            order_id, 75.0, PaymentMethod.CREDIT_CARD, payment_info
        )
        
        history = self.payment_service.get_payment_history(order_id)
        
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['order_id'], order_id)
        self.assertEqual(history[0]['amount'], 75.0)

    def test_get_payment_history_no_payments(self) -> None:
        """Test getting payment history for order with no payments."""
        history = self.payment_service.get_payment_history(999)
        
        self.assertEqual(len(history), 0)


if __name__ == '__main__':
    unittest.main()
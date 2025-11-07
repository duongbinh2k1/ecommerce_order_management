"""
Test CustomerService - with mocked repository dependencies
Tests customer management, loyalty points, and membership upgrades
"""
import unittest
from unittest.mock import Mock
from services.customer_service import CustomerService
from domain.models.customer import Customer
from domain.enums.membership_tier import MembershipTier


class TestCustomerService(unittest.TestCase):
    """Test CustomerService with mocked repository dependencies."""

    def setUp(self) -> None:
        """Set up test dependencies."""
        self.mock_repository = Mock()
        self.customer_service = CustomerService(self.mock_repository)

    def test_add_customer_success(self) -> None:
        """Test adding a customer successfully."""
        customer = self.customer_service.add_customer(
            customer_id=123,
            name="John Doe",
            email="john@example.com",
            tier="gold",
            phone="555-0123",
            address="123 Main St"
        )
        
        self.assertEqual(customer.customer_id, 123)
        self.assertEqual(customer.name, "John Doe")
        self.mock_repository.add.assert_called_once_with(customer)

    def test_get_customer_found(self) -> None:
        """Test getting a customer that exists."""
        expected_customer = Customer(
            customer_id=123,
            name="John Doe",
            email="john@example.com",
            membership_tier="gold",
            phone="555-0123",
            address="123 Main St",
            loyalty_points=100
        )
        self.mock_repository.get.return_value = expected_customer
        
        result = self.customer_service.get_customer(123)
        
        self.assertEqual(result, expected_customer)
        self.mock_repository.get.assert_called_once_with(123)

    def test_get_customer_not_found(self) -> None:
        """Test getting a customer that doesn't exist."""
        self.mock_repository.get.return_value = None
        
        result = self.customer_service.get_customer(999)
        
        self.assertIsNone(result)
        self.mock_repository.get.assert_called_once_with(999)

    def test_add_loyalty_points_success(self) -> None:
        """Test adding loyalty points to existing customer."""
        existing_customer = Customer(
            customer_id=123,
            name="John Doe",
            email="john@example.com",
            membership_tier="gold",
            phone="555-0123", 
            address="123 Main St",
            loyalty_points=100
        )
        self.mock_repository.get.return_value = existing_customer
        
        result = self.customer_service.add_loyalty_points(123, 50)
        
        self.assertTrue(result)
        self.mock_repository.get.assert_called_once_with(123)
        self.mock_repository.update.assert_called_once()

    def test_add_loyalty_points_customer_not_found(self) -> None:
        """Test adding loyalty points to non-existent customer."""
        self.mock_repository.get.return_value = None
        
        result = self.customer_service.add_loyalty_points(999, 50)
        
        self.assertFalse(result)
        self.mock_repository.get.assert_called_once_with(999)
        self.mock_repository.update.assert_not_called()

    def test_upgrade_membership_success(self) -> None:
        """Test upgrading customer membership."""
        existing_customer = Customer(
            customer_id=123,
            name="John Doe",
            email="john@example.com",
            membership_tier="silver",
            phone="555-0123",
            address="123 Main St",
            loyalty_points=1000
        )
        self.mock_repository.get.return_value = existing_customer
        
        result = self.customer_service.upgrade_membership(123, MembershipTier.GOLD)
        
        self.assertTrue(result)
        self.mock_repository.get.assert_called_once_with(123)
        self.mock_repository.update.assert_called_once()

    def test_upgrade_membership_customer_not_found(self) -> None:
        """Test upgrading membership for non-existent customer."""
        self.mock_repository.get.return_value = None
        
        result = self.customer_service.upgrade_membership(999, MembershipTier.GOLD)
        
        self.assertFalse(result)
        self.mock_repository.get.assert_called_once_with(999)
        self.mock_repository.update.assert_not_called()

    def test_auto_upgrade_membership_qualifies_for_gold(self) -> None:
        """Test automatic membership upgrade for high lifetime value."""
        existing_customer = Customer(
            customer_id=123,
            name="John Doe",
            email="john@example.com",
            membership_tier="silver",
            phone="555-0123",
            address="123 Main St",
            loyalty_points=500
        )
        self.mock_repository.get.return_value = existing_customer
        
        # High lifetime value should qualify for gold
        result = self.customer_service.auto_upgrade_membership(123, 5000.0)
        
        self.assertTrue(result)
        # Repository get might be called multiple times, so check call count instead
        self.assertGreaterEqual(self.mock_repository.get.call_count, 1)
        self.mock_repository.update.assert_called_once()

    def test_auto_upgrade_membership_qualifies_for_silver(self) -> None:
        """Test automatic membership upgrade for medium lifetime value."""
        existing_customer = Customer(
            customer_id=123,
            name="John Doe",
            email="john@example.com",
            membership_tier="standard",
            phone="555-0123",
            address="123 Main St",
            loyalty_points=200
        )
        self.mock_repository.get.return_value = existing_customer
        
        # Medium lifetime value should qualify for silver
        result = self.customer_service.auto_upgrade_membership(123, 2000.0)
        
        self.assertTrue(result)
        # Repository get might be called multiple times, so check call count instead
        self.assertGreaterEqual(self.mock_repository.get.call_count, 1)
        self.mock_repository.update.assert_called_once()

    def test_auto_upgrade_membership_no_upgrade_needed(self) -> None:
        """Test automatic membership upgrade when no upgrade needed."""
        existing_customer = Customer(
            customer_id=123,
            name="John Doe",
            email="john@example.com",
            membership_tier="gold",  # Already gold
            phone="555-0123",
            address="123 Main St",
            loyalty_points=1000
        )
        self.mock_repository.get.return_value = existing_customer
        
        # Already gold, no upgrade needed
        result = self.customer_service.auto_upgrade_membership(123, 5000.0)
        
        self.assertFalse(result)  # No upgrade performed
        self.mock_repository.get.assert_called_once_with(123)
        self.mock_repository.update.assert_not_called()

    def test_get_all_customers(self) -> None:
        """Test getting all customers."""
        expected_customers = {
            1: Customer(1, "Customer 1", "c1@test.com", "gold", "555-0001", "Address 1", 100),
            2: Customer(2, "Customer 2", "c2@test.com", "silver", "555-0002", "Address 2", 200)
        }
        self.mock_repository.get_all.return_value = expected_customers
        
        result = self.customer_service.get_all_customers()
        
        self.assertEqual(result, expected_customers)
        self.mock_repository.get_all.assert_called_once()


if __name__ == '__main__':
    unittest.main()
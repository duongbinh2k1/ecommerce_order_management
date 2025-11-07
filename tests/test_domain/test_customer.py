"""
Test Customer domain model - validation and business rules
Tests the refactored Customer class business logic
"""
import unittest
from domain.models.customer import Customer
from domain.enums.membership_tier import MembershipTier


class TestCustomer(unittest.TestCase):
    """Test Customer domain model validation and business rules."""

    def test_customer_creation_valid(self):
        """Test creating Customer with valid data."""
        customer = Customer(
            customer_id="123",
            name="John Doe",
            email="john@example.com",
            membership_tier="gold",
            phone="555-0123",
            address="123 Main St",
            loyalty_points=100
        )
        
        self.assertEqual(customer.customer_id, "123")
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.email.value, "john@example.com")
        self.assertEqual(customer.membership_tier, MembershipTier.GOLD)
        self.assertEqual(customer.phone.value, "555-0123")
        self.assertEqual(customer.address.value, "123 Main St")
        self.assertEqual(customer.loyalty_points, 100)

    def test_customer_validation_invalid_email(self):
        """Test Customer validation - should reject invalid email."""
        with self.assertRaises(ValueError):
            Customer(
                customer_id="123",
                name="John Doe",
                email="invalid-email",  # Invalid email format
                membership_tier="gold",
                phone="555-0123",
                address="123 Main St",
                loyalty_points=100
            )

    def test_customer_validation_empty_name(self):
        """Test Customer validation - should reject empty name."""
        with self.assertRaises(ValueError):
            Customer(
                customer_id="123",
                name="",  # Invalid empty name
                email="john@example.com",
                membership_tier="gold",
                phone="555-0123",
                address="123 Main St",
                loyalty_points=100
            )

    def test_customer_validation_negative_loyalty_points(self):
        """Test Customer validation - should reject negative loyalty points."""
        with self.assertRaises(ValueError):
            Customer(
                customer_id="123",
                name="John Doe",
                email="john@example.com",
                membership_tier="gold",
                phone="555-0123",
                address="123 Main St",
                loyalty_points=-10  # Invalid negative loyalty points
            )

    def test_customer_validation_invalid_membership_tier(self):
        """Test Customer validation - should reject invalid membership tier."""
        with self.assertRaises(ValueError):
            Customer(
                customer_id="123",
                name="John Doe",
                email="john@example.com",
                membership_tier="invalid_tier",  # Invalid tier
                phone="555-0123",
                address="123 Main St",
                loyalty_points=100
            )

    def test_customer_membership_tiers(self):
        """Test different membership tiers."""
        # Gold member
        gold_customer = Customer(
            customer_id="1",
            name="Gold Member",
            email="gold@example.com",
            membership_tier="gold",
            phone="555-0001",
            address="Gold St",
            loyalty_points=1000
        )
        self.assertEqual(gold_customer.membership_tier, MembershipTier.GOLD)
        
        # Silver member
        silver_customer = Customer(
            customer_id="2",
            name="Silver Member",
            email="silver@example.com",
            membership_tier="silver",
            phone="555-0002",
            address="Silver St",
            loyalty_points=500
        )
        self.assertEqual(silver_customer.membership_tier, MembershipTier.SILVER)
        
        # Standard member
        standard_customer = Customer(
            customer_id="3",
            name="Standard Member",
            email="standard@example.com",
            membership_tier="standard",
            phone="555-0003",
            address="Standard St",
            loyalty_points=100
        )
        self.assertEqual(standard_customer.membership_tier, MembershipTier.STANDARD)

    def test_customer_object_attributes(self):
        """Test Customer object creation and attributes."""
        customer = Customer(
            customer_id="123",
            name="John Doe",
            email="john@example.com",
            membership_tier="gold",
            phone="555-0123",
            address="123 Main St",
            loyalty_points=100
        )
        
        # Test object attributes
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.customer_id, "123")
        self.assertEqual(customer.loyalty_points, 100)


if __name__ == '__main__':
    unittest.main()
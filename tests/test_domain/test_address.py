"""
Test Address value object validation
"""
import unittest
from domain.value_objects.address import Address


class TestAddress(unittest.TestCase):
    """Test Address value object validation."""

    def test_address_creation_valid(self) -> None:
        """Test creating Address with valid values."""
        valid_addresses = [
            "123 Main Street, City, State",
            "456 Oak Avenue",
            "789 Elm St, Apt 4B, Springfield, IL 62701",
            "Short St"  # Minimum length (5 chars after strip)
        ]
        
        for addr_str in valid_addresses:
            address = Address(addr_str)
            self.assertEqual(address.value, addr_str)
            self.assertEqual(str(address), addr_str)

    def test_address_creation_invalid(self) -> None:
        """Test creating Address with invalid values."""
        invalid_addresses = [
            "",  # Empty string
            "   ",  # Only whitespace
            "123",  # Too short (less than 5 chars)
            "A" * 201,  # Too long (more than 200 chars)
        ]
        
        for addr_str in invalid_addresses:
            with self.assertRaises(ValueError):
                Address(addr_str)

    def test_address_contains_state(self) -> None:
        """Test Address contains method for state codes."""
        address = Address("123 Main St, Springfield, CA 90210")
        
        self.assertTrue(address.contains("CA"))
        self.assertFalse(address.contains("NY"))
        self.assertFalse(address.contains("TX"))

    def test_address_equality(self) -> None:
        """Test Address equality comparison."""
        addr1 = Address("123 Main Street")
        addr2 = Address("123 Main Street")
        addr3 = Address("456 Oak Avenue")
        
        self.assertEqual(addr1, addr2)
        self.assertNotEqual(addr1, addr3)

    def test_address_hash(self) -> None:
        """Test Address can be used in sets and as dict keys."""
        addr1 = Address("123 Main Street")
        addr2 = Address("123 Main Street")
        
        addr_set = {addr1, addr2}
        self.assertEqual(len(addr_set), 1)  # Should be deduplicated
        
        addr_dict = {addr1: "value"}
        self.assertEqual(addr_dict[addr2], "value")  # Should work as dict key


if __name__ == '__main__':
    unittest.main()
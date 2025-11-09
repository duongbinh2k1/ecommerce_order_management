"""
Test PhoneNumber value object validation
"""
import unittest
from domain.value_objects.phone_number import PhoneNumber


class TestPhoneNumber(unittest.TestCase):
    """Test PhoneNumber value object validation."""

    def test_phone_creation_valid(self) -> None:
        """Test creating PhoneNumber with valid formats."""
        valid_phones = [
            "12345",  # Minimum 5 digits
            "1234567",  # 7 digits
            "0123456789",  # Basic 10 digits
            "01234567890",  # 11 digits
            "+1 234 567 8901",  # International with spaces
            "(123) 456-7890",  # US format with parentheses
            "+84-123-456-789",  # International with hyphens
            "555-0123",  # 7 digits with separator
            None  # Should be allowed
        ]
        
        for phone_str in valid_phones:
            phone = PhoneNumber(phone_str)
            self.assertEqual(phone.value, phone_str)

    def test_phone_creation_invalid(self) -> None:
        """Test creating PhoneNumber with invalid formats."""
        invalid_phones = [
            "1234",  # Too short (less than 5 digits)
            "abc123456789",  # Contains letters
            "123!@#456789",  # Contains special chars (non-phone)
            "12345678901234567890",  # Too long (more than 15 digits)
            "",  # Empty string
            "   ",  # Only whitespace
        ]
        
        for phone_str in invalid_phones:
            with self.assertRaises(ValueError):
                PhoneNumber(phone_str)

    def test_phone_truthiness(self) -> None:
        """Test PhoneNumber truthiness check."""
        phone_valid = PhoneNumber("0123456789")
        phone_none = PhoneNumber(None)
        
        self.assertTrue(bool(phone_valid))
        self.assertFalse(bool(phone_none))

    def test_phone_equality(self) -> None:
        """Test PhoneNumber equality comparison."""
        phone1 = PhoneNumber("0123456789")
        phone2 = PhoneNumber("0123456789")
        phone3 = PhoneNumber("0987654321")
        phone_none = PhoneNumber(None)
        
        self.assertEqual(phone1, phone2)
        self.assertNotEqual(phone1, phone3)
        self.assertNotEqual(phone1, phone_none)

    def test_phone_string_representation(self) -> None:
        """Test PhoneNumber string representation."""
        phone = PhoneNumber("0123456789")
        phone_none = PhoneNumber(None)
        
        self.assertEqual(str(phone), "0123456789")
        self.assertEqual(str(phone_none), "")


if __name__ == '__main__':
    unittest.main()
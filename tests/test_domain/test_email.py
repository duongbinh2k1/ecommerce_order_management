"""
Test Email value object validation
"""
import unittest
from domain.value_objects.email import Email


class TestEmail(unittest.TestCase):
    """Test Email value object validation."""

    def test_email_creation_valid(self) -> None:
        """Test creating Email with valid formats."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "123@test.org",
            "a@b.c"
        ]
        
        for email_str in valid_emails:
            email = Email(email_str)
            self.assertEqual(email.value, email_str)
            self.assertEqual(str(email), email_str)

    def test_email_creation_invalid(self) -> None:
        """Test creating Email with invalid formats."""
        invalid_emails = [
            "",  # Empty string
            "invalid-email",  # No @ symbol
            "@domain.com",  # No local part
            "user@",  # No domain
            "   ",  # Only whitespace
        ]
        
        for email_str in invalid_emails:
            with self.assertRaises(ValueError):
                Email(email_str)

    def test_email_equality(self) -> None:
        """Test Email equality comparison."""
        email1 = Email("test@example.com")
        email2 = Email("test@example.com")
        email3 = Email("different@example.com")
        
        self.assertEqual(email1, email2)
        self.assertNotEqual(email1, email3)
        self.assertNotEqual(email1, "test@example.com")  # Different type

    def test_email_hash(self) -> None:
        """Test Email can be used in sets and as dict keys."""
        email1 = Email("test@example.com")
        email2 = Email("test@example.com")
        
        email_set = {email1, email2}
        self.assertEqual(len(email_set), 1)  # Should be deduplicated
        
        email_dict = {email1: "value"}
        self.assertEqual(email_dict[email2], "value")  # Should work as dict key


if __name__ == '__main__':
    unittest.main()
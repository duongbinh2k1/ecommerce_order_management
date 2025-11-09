"""
Email value object - extracted from Customer.email validation needs
Used in: Customer, Supplier
"""


class Email:
    def __init__(self, email: str) -> None:
        self.__validate(email)
        self.__email = email.strip()

    def __validate(self, email: str) -> None:
        """Validate email format"""
        if not email or not email.strip():
            raise ValueError(f"Invalid email: {email}")
        
        email = email.strip()
        if '@' not in email:
            raise ValueError(f"Invalid email: {email}")
        
        # Split by @ to check local and domain parts
        parts = email.split('@')
        if len(parts) != 2:
            raise ValueError(f"Invalid email: {email}")
        
        local_part, domain_part = parts
        if not local_part or not domain_part:
            raise ValueError(f"Invalid email: {email}")

    @property
    def value(self) -> str:
        """Get the email string value"""
        return self.__email

    def __str__(self) -> str:
        return self.__email

    def __repr__(self) -> str:
        return f"Email('{self.__email}')"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Email):
            return self.__email == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.__email)

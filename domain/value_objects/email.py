"""
Email value object - extracted from Customer.email validation needs
Used in: Customer, Supplier
"""


class Email:
    def __init__(self, email: str) -> None:
        self.__email = email
        self.__validate()

    def __validate(self) -> None:
        """Validate email format"""
        if not self.__email or '@' not in self.__email:
            raise ValueError(f"Invalid email: {self.__email}")

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

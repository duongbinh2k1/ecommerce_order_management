"""
Address value object - extracted from Customer.address
Used in: Customer, for tax rate calculation
"""


class Address:
    def __init__(self, address: str) -> None:
        self.__validate(address)
        self.__address = address

    def __validate(self, address: str) -> None:
        """Validate address format"""
        if not address or not address.strip():
            raise ValueError("Address cannot be empty")
        if len(address.strip()) < 5:
            raise ValueError(f"Address too short (minimum 5 characters): {address}")
        if len(address) > 200:
            raise ValueError(f"Address too long (maximum 200 characters): {address}")

    @property
    def value(self) -> str:
        """Get the address string value"""
        return self.__address

    def contains(self, state_code: str) -> bool:
        """Check if address contains a state code (e.g., 'CA', 'NY', 'TX')"""
        return state_code in self.__address if self.__address else False

    def __str__(self) -> str:
        return self.__address if self.__address else ""

    def __repr__(self) -> str:
        return f"Address('{self.__address}')"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Address):
            return self.__address == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.__address)

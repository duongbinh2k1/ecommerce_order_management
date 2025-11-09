"""
PricingResult value object - for structured pricing calculation results
Used by: PricingService.apply_all_discounts() return value
"""
from typing import Union
from domain.value_objects.money import Money


class PricingResult:
    """Value object representing essential pricing calculation results."""
    
    def __init__(
        self,
        original_subtotal: Union[int, float],
        loyalty_points_used: int,
        subtotal_after_loyalty: Union[int, float],
        total_weight: Union[int, float]
    ) -> None:
        """
        Initialize pricing result with only essential fields used by OrderService.
        
        Args:
            original_subtotal: Base subtotal before any discounts
            loyalty_points_used: Number of loyalty points applied
            subtotal_after_loyalty: Final subtotal after all discounts
            total_weight: Total weight of all order items
        """
        self.__validate(
            original_subtotal, loyalty_points_used, subtotal_after_loyalty, total_weight
        )
        
        self.__original_subtotal = Money(original_subtotal)
        self.__loyalty_points_used = int(loyalty_points_used)
        self.__subtotal_after_loyalty = Money(subtotal_after_loyalty)
        self.__total_weight = float(total_weight)

    def __validate(
        self,
        original_subtotal: Union[int, float],
        loyalty_points_used: int,
        subtotal_after_loyalty: Union[int, float],
        total_weight: Union[int, float]
    ) -> None:
        """Validate pricing result business rules."""
        if original_subtotal < 0:
            raise ValueError("Original subtotal cannot be negative")
        if subtotal_after_loyalty < 0:
            raise ValueError("Subtotal after loyalty cannot be negative")
        if loyalty_points_used < 0:
            raise ValueError("Loyalty points used cannot be negative")
        if total_weight < 0:
            raise ValueError("Total weight cannot be negative")

    # Properties for read-only access
    @property
    def original_subtotal(self) -> Money:
        """Get original subtotal before discounts."""
        return self.__original_subtotal

    @property
    def loyalty_points_used(self) -> int:
        """Get number of loyalty points used."""
        return self.__loyalty_points_used

    @property
    def subtotal_after_loyalty(self) -> Money:
        """Get final subtotal after all discounts applied."""
        return self.__subtotal_after_loyalty

    @property
    def total_weight(self) -> float:
        """Get total weight of order items."""
        return self.__total_weight

    def __str__(self) -> str:
        """String representation of pricing result."""
        return (
            f"PricingResult(original={self.__original_subtotal}, "
            f"final={self.__subtotal_after_loyalty}, "
            f"points_used={self.__loyalty_points_used}, "
            f"weight={self.__total_weight})"
        )

    def __repr__(self) -> str:
        """Detailed representation of pricing result."""
        return (
            f"PricingResult("
            f"original_subtotal={self.__original_subtotal.value}, "
            f"loyalty_points_used={self.__loyalty_points_used}, "
            f"subtotal_after_loyalty={self.__subtotal_after_loyalty.value}, "
            f"total_weight={self.__total_weight})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality with another PricingResult."""
        if not isinstance(other, PricingResult):
            return False
        return (
            self.__original_subtotal == other.original_subtotal and
            self.__loyalty_points_used == other.loyalty_points_used and
            self.__subtotal_after_loyalty == other.subtotal_after_loyalty and
            abs(self.__total_weight - other.total_weight) < 0.01
        )
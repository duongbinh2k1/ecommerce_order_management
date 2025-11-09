"""Test cases for Shipment domain model."""
import unittest
from domain.models.shipment import Shipment
from domain.enums.shipment_status import ShipmentStatus
from domain.enums.shipping_method import ShippingMethod
from domain.value_objects.address import Address


class TestShipment(unittest.TestCase):
    """Test cases for Shipment domain model."""

    def test_shipment_creation_valid(self) -> None:
        """Test creating a valid shipment."""
        shipment = Shipment(
            shipment_id=1,
            order_id=100,
            tracking_number="TRACK12345",
            shipping_method="express",
            address="123 Main St, City, State",
            status="pending"
        )
        
        self.assertEqual(shipment.shipment_id, 1)
        self.assertEqual(shipment.order_id, 100)
        self.assertEqual(shipment.tracking_number, "TRACK12345")
        self.assertEqual(shipment.shipping_method, ShippingMethod.EXPRESS)
        self.assertIsInstance(shipment.address, Address)
        self.assertEqual(shipment.address.value, "123 Main St, City, State")
        self.assertEqual(shipment.status, ShipmentStatus.PENDING)

    def test_shipment_creation_default_status(self) -> None:
        """Test creating shipment with default status."""
        shipment = Shipment(
            shipment_id=2,
            order_id=200,
            tracking_number="TRACK67890",
            shipping_method="standard",
            address="456 Oak Ave, City, State"
        )
        
        self.assertEqual(shipment.status, ShipmentStatus.PENDING)

    def test_shipment_creation_invalid_id(self) -> None:
        """Test shipment creation with invalid shipment ID."""
        with self.assertRaises(ValueError) as context:
            Shipment(
                shipment_id=0,
                order_id=100,
                tracking_number="TRACK12345",
                shipping_method="express",
                address="123 Main St"
            )
        
        self.assertEqual(str(context.exception), "Shipment ID must be positive")

    def test_shipment_creation_invalid_order_id(self) -> None:
        """Test shipment creation with invalid order ID."""
        with self.assertRaises(ValueError) as context:
            Shipment(
                shipment_id=1,
                order_id=-1,
                tracking_number="TRACK12345",
                shipping_method="express",
                address="123 Main St"
            )
        
        self.assertEqual(str(context.exception), "Order ID must be positive")

    def test_shipment_creation_empty_tracking_number(self) -> None:
        """Test shipment creation with empty tracking number."""
        with self.assertRaises(ValueError) as context:
            Shipment(
                shipment_id=1,
                order_id=100,
                tracking_number="",
                shipping_method="express",
                address="123 Main St"
            )
        
        self.assertEqual(str(context.exception), "Tracking number cannot be empty")

    def test_shipment_creation_invalid_shipping_method(self) -> None:
        """Test shipment creation with invalid shipping method."""
        with self.assertRaises(ValueError):
            Shipment(
                shipment_id=1,
                order_id=100,
                tracking_number="TRACK12345",
                shipping_method="invalid_method",
                address="123 Main St"
            )

    def test_shipment_creation_invalid_status(self) -> None:
        """Test shipment creation with invalid status."""
        with self.assertRaises(ValueError):
            Shipment(
                shipment_id=1,
                order_id=100,
                tracking_number="TRACK12345",
                shipping_method="express",
                address="123 Main St",
                status="invalid_status"
            )

    def test_shipment_status_setter(self) -> None:
        """Test updating shipment status."""
        shipment = Shipment(
            shipment_id=1,
            order_id=100,
            tracking_number="TRACK12345",
            shipping_method="express",
            address="123 Main St"
        )
        
        shipment.status = "in_transit"
        self.assertEqual(shipment.status, ShipmentStatus.IN_TRANSIT)
        
        shipment.status = "delivered"
        self.assertEqual(shipment.status, ShipmentStatus.DELIVERED)

    def test_shipment_status_setter_invalid(self) -> None:
        """Test updating shipment status with invalid value."""
        shipment = Shipment(
            shipment_id=1,
            order_id=100,
            tracking_number="TRACK12345",
            shipping_method="express",
            address="123 Main St"
        )
        
        with self.assertRaises(ValueError):
            shipment.status = "invalid_status"

    def test_shipment_string_representation(self) -> None:
        """Test string representation of shipment."""
        shipment = Shipment(
            shipment_id=1,
            order_id=100,
            tracking_number="TRACK12345",
            shipping_method="express",
            address="123 Main St"
        )
        
        self.assertEqual(str(shipment), "Shipment(1: TRACK12345)")

    def test_shipment_repr(self) -> None:
        """Test repr of shipment."""
        shipment = Shipment(
            shipment_id=1,
            order_id=100,
            tracking_number="TRACK12345",
            shipping_method="express",
            address="123 Main St"
        )
        
        expected_repr = "Shipment(id=1, tracking='TRACK12345', status=pending)"
        self.assertEqual(repr(shipment), expected_repr)

    def test_shipment_equality(self) -> None:
        """Test shipment equality based on ID."""
        shipment1 = Shipment(
            shipment_id=1,
            order_id=100,
            tracking_number="TRACK12345",
            shipping_method="express",
            address="123 Main St"
        )
        
        shipment2 = Shipment(
            shipment_id=1,
            order_id=200,  # Different order ID
            tracking_number="TRACK67890",  # Different tracking
            shipping_method="standard",
            address="456 Oak Ave"
        )
        
        shipment3 = Shipment(
            shipment_id=2,
            order_id=100,
            tracking_number="TRACK12345",
            shipping_method="express",
            address="123 Main St"
        )
        
        # Same ID should be equal
        self.assertEqual(shipment1, shipment2)
        # Different ID should not be equal
        self.assertNotEqual(shipment1, shipment3)
        # Not shipment object should not be equal
        self.assertNotEqual(shipment1, "not a shipment")

    def test_shipment_hash(self) -> None:
        """Test shipment hash based on ID."""
        shipment1 = Shipment(
            shipment_id=1,
            order_id=100,
            tracking_number="TRACK12345",
            shipping_method="express",
            address="123 Main St"
        )
        
        shipment2 = Shipment(
            shipment_id=1,
            order_id=200,
            tracking_number="TRACK67890",
            shipping_method="standard",
            address="456 Oak Ave"
        )
        
        # Same ID should have same hash
        self.assertEqual(hash(shipment1), hash(shipment2))
        
        # Can be used in sets
        shipment_set = {shipment1, shipment2}
        self.assertEqual(len(shipment_set), 1)  # Only one unique shipment

    def test_all_shipping_methods(self) -> None:
        """Test shipment with all shipping methods."""
        methods = ["standard", "express", "overnight"]
        
        for i, method in enumerate(methods, 1):
            shipment = Shipment(
                shipment_id=i,
                order_id=100 + i,
                tracking_number=f"TRACK{i}",
                shipping_method=method,
                address="123 Main St"
            )
            
            self.assertEqual(shipment.shipping_method, ShippingMethod(method))

    def test_all_shipment_statuses(self) -> None:
        """Test shipment with all statuses."""
        statuses = ["pending", "in_transit", "delivered", "cancelled", "returned"]
        
        for i, status in enumerate(statuses, 1):
            shipment = Shipment(
                shipment_id=i,
                order_id=100 + i,
                tracking_number=f"TRACK{i}",
                shipping_method="standard",
                address="123 Main St",
                status=status
            )
            
            self.assertEqual(shipment.status, ShipmentStatus(status))


if __name__ == '__main__':
    unittest.main()
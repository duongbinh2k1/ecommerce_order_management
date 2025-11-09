"""Test cases for ShipmentService."""
import unittest
from unittest.mock import Mock
from services.shipment_service import ShipmentService
from domain.enums.shipping_method import ShippingMethod
from domain.enums.shipment_status import ShipmentStatus
from domain.models.shipment import Shipment


class TestShipmentService(unittest.TestCase):
    """Test cases for ShipmentService class."""

    def setUp(self) -> None:
        """Set up test dependencies."""
        self.shipment_repository = Mock()
        self.shipment_repository.get_next_id.return_value = 1
        
        self.shipment_service = ShipmentService(self.shipment_repository)

    def test_create_shipment_success(self) -> None:
        """Test creating shipment successfully."""
        tracking = self.shipment_service.create_shipment(
            order_id=123,
            shipping_method=ShippingMethod.EXPRESS,
            address="123 Main St"
        )
        
        self.assertTrue(tracking.startswith("TRACK123"))
        self.shipment_repository.add.assert_called_once()
        
        # Verify shipment data
        call_args = self.shipment_repository.add.call_args[0][0]
        self.assertIsInstance(call_args, Shipment)
        self.assertEqual(call_args.order_id, 123)
        self.assertEqual(call_args.shipping_method.value, ShippingMethod.EXPRESS.value)
        self.assertEqual(call_args.address.value, "123 Main St")
        self.assertEqual(call_args.status, ShipmentStatus.PENDING)

    def test_update_shipment_status_success(self) -> None:
        """Test updating shipment status successfully."""
        mock_shipment = Mock(spec=Shipment)
        mock_shipment.status = ShipmentStatus.PENDING
        
        self.shipment_repository.find_by_tracking_number.return_value = mock_shipment
        
        result = self.shipment_service.update_shipment_status('TRACK123', 'in_transit')
        
        self.assertTrue(result)
        self.shipment_repository.find_by_tracking_number.assert_called_once_with('TRACK123')
        self.assertEqual(mock_shipment.status, 'in_transit')
        self.shipment_repository.update.assert_called_once_with(mock_shipment)

    def test_update_shipment_status_not_found(self) -> None:
        """Test updating shipment status when tracking number not found."""
        self.shipment_repository.find_by_tracking_number.return_value = None
        
        result = self.shipment_service.update_shipment_status('NOTFOUND', 'delivered')
        
        self.assertFalse(result)
        self.shipment_repository.update.assert_not_called()

    def test_get_tracking_info_found(self) -> None:
        """Test getting tracking info when shipment exists."""
        mock_shipment = Mock(spec=Shipment)
        mock_shipment.tracking_number = 'TRACK123'
        
        self.shipment_repository.find_by_tracking_number.return_value = mock_shipment
        
        result = self.shipment_service.get_tracking_info('TRACK123')
        
        self.assertEqual(result, mock_shipment)
        self.shipment_repository.find_by_tracking_number.assert_called_once_with('TRACK123')

    def test_get_tracking_info_not_found(self) -> None:
        """Test getting tracking info when shipment doesn't exist."""
        self.shipment_repository.find_by_tracking_number.return_value = None
        
        result = self.shipment_service.get_tracking_info('NOTFOUND')
        
        self.assertIsNone(result)

    def test_get_shipments_by_order(self) -> None:
        """Test getting shipments by order ID."""
        mock_shipments = [Mock(spec=Shipment), Mock(spec=Shipment)]
        self.shipment_repository.find_by_order_id.return_value = mock_shipments
        
        result = self.shipment_service.get_shipments_by_order(123)
        
        self.assertEqual(result, mock_shipments)
        self.shipment_repository.find_by_order_id.assert_called_once_with(123)

    def test_get_all_shipments(self) -> None:
        """Test getting all shipments."""
        mock_shipments = [Mock(spec=Shipment), Mock(spec=Shipment)]
        self.shipment_repository.get_all.return_value = mock_shipments
        
        result = self.shipment_service.get_all_shipments()
        
        self.assertEqual(result, mock_shipments)
        self.shipment_repository.get_all.assert_called_once()

    def test_ship_order(self) -> None:
        """Test shipping an order."""
        mock_shipment = Mock(spec=Shipment)
        self.shipment_repository.find_by_tracking_number.return_value = mock_shipment
        
        tracking = self.shipment_service.ship_order(
            order_id=456,
            shipping_method=ShippingMethod.STANDARD,
            address="456 Oak Ave"
        )
        
        self.assertTrue(tracking.startswith("TRACK456"))
        # Should create shipment and update status
        self.shipment_repository.add.assert_called_once()
        self.shipment_repository.update.assert_called_once()

    def test_cancel_shipment_success(self) -> None:
        """Test cancelling a pending shipment."""
        mock_shipment = Mock(spec=Shipment)
        mock_shipment.status = ShipmentStatus.PENDING
        
        self.shipment_repository.find_by_tracking_number.return_value = mock_shipment
        
        result = self.shipment_service.cancel_shipment('TRACK123')
        
        self.assertTrue(result)
        self.assertEqual(mock_shipment.status, ShipmentStatus.CANCELLED.value)
        self.shipment_repository.update.assert_called_once()

    def test_cancel_shipment_already_shipped(self) -> None:
        """Test cancelling a shipment that's already in transit."""
        mock_shipment = Mock(spec=Shipment)
        mock_shipment.status = ShipmentStatus.IN_TRANSIT
        
        self.shipment_repository.find_by_tracking_number.return_value = mock_shipment
        
        result = self.shipment_service.cancel_shipment('TRACK123')
        
        self.assertFalse(result)
        self.shipment_repository.update.assert_not_called()

    def test_cancel_shipment_not_found(self) -> None:
        """Test cancelling a non-existent shipment."""
        self.shipment_repository.find_by_tracking_number.return_value = None
        
        result = self.shipment_service.cancel_shipment('NOTFOUND')
        
        self.assertFalse(result)

    def test_mark_delivered(self) -> None:
        """Test marking shipment as delivered."""
        mock_shipment = Mock(spec=Shipment)
        self.shipment_repository.find_by_tracking_number.return_value = mock_shipment
        
        result = self.shipment_service.mark_delivered('TRACK123')
        
        self.assertTrue(result)
        self.assertEqual(mock_shipment.status, ShipmentStatus.DELIVERED.value)


if __name__ == '__main__':
    unittest.main()
"""
Test SupplierService - supplier management functionality
Tests supplier creation, reliability tracking, and notifications
"""
import unittest
from unittest.mock import Mock
from services.supplier_service import SupplierService
from domain.models.supplier import Supplier


class TestSupplierService(unittest.TestCase):
    """Test SupplierService supplier management functionality."""

    def setUp(self) -> None:
        """Set up test dependencies."""
        self.supplier_repository = Mock()
        self.supplier_service = SupplierService(self.supplier_repository)

        # Create mock supplier
        self.supplier = Supplier(
            supplier_id=1,
            name="Test Supplier",
            email="supplier@test.com",
            reliability_score=0.85
        )

    def test_add_supplier(self) -> None:
        """Test adding a new supplier."""
        result = self.supplier_service.add_supplier(
            2,
            "New Supplier",
            "new@supplier.com",
            0.75
        )

        self.assertIsInstance(result, Supplier)
        self.assertEqual(result.supplier_id, 2)
        self.assertEqual(result.name, "New Supplier")
        self.assertEqual(result.email.value, "new@supplier.com")
        self.assertEqual(result.reliability_score, 0.75)
        
        self.supplier_repository.add.assert_called_once_with(result)

    def test_get_supplier_found(self) -> None:
        """Test getting an existing supplier."""
        self.supplier_repository.get.return_value = self.supplier
        
        result = self.supplier_service.get_supplier(1)
        
        self.assertEqual(result, self.supplier)
        self.supplier_repository.get.assert_called_once_with(1)

    def test_get_supplier_not_found(self) -> None:
        """Test getting a non-existent supplier."""
        self.supplier_repository.get.return_value = None
        
        result = self.supplier_service.get_supplier(999)
        
        self.assertIsNone(result)

    def test_get_reliable_suppliers_default_threshold(self) -> None:
        """Test getting reliable suppliers with default threshold."""
        reliable_supplier = Supplier(
            supplier_id=2,
            name="Reliable Supplier",
            email="reliable@test.com",
            reliability_score=0.9
        )
        
        unreliable_supplier = Supplier(
            supplier_id=3,
            name="Unreliable Supplier",
            email="unreliable@test.com",
            reliability_score=0.5
        )
        
        self.supplier_repository.get_all.return_value = {
            2: reliable_supplier,
            3: unreliable_supplier,
            1: self.supplier  # 0.85 reliability
        }
        
        result = self.supplier_service.get_reliable_suppliers()
        
        self.assertEqual(len(result), 2)  # Only suppliers with >= 0.7 reliability
        supplier_ids = [s.supplier_id for s in result]
        self.assertIn(2, supplier_ids)
        self.assertIn(1, supplier_ids)
        self.assertNotIn(3, supplier_ids)

    def test_get_reliable_suppliers_custom_threshold(self) -> None:
        """Test getting reliable suppliers with custom threshold."""
        supplier1 = Supplier(
            supplier_id=4,
            name="Supplier 1",
            email="sup1@test.com",
            reliability_score=0.6
        )
        
        supplier2 = Supplier(
            supplier_id=5,
            name="Supplier 2",
            email="sup2@test.com",
            reliability_score=0.8
        )
        
        self.supplier_repository.get_all.return_value = {
            4: supplier1,
            5: supplier2,
            1: self.supplier  # 0.85 reliability
        }
        
        # Test with threshold of 0.75
        result = self.supplier_service.get_reliable_suppliers(0.75)
        
        self.assertEqual(len(result), 2)  # Only suppliers with >= 0.75 reliability
        supplier_ids = [s.supplier_id for s in result]
        self.assertIn(5, supplier_ids)
        self.assertIn(1, supplier_ids)
        self.assertNotIn(4, supplier_ids)

    def test_get_reliable_suppliers_none_meet_threshold(self) -> None:
        """Test getting reliable suppliers when none meet threshold."""
        unreliable_supplier = Supplier(
            supplier_id=6,
            name="Unreliable Supplier",
            email="unreliable@test.com",
            reliability_score=0.3
        )
        
        self.supplier_repository.get_all.return_value = {
            6: unreliable_supplier
        }
        
        result = self.supplier_service.get_reliable_suppliers(0.8)
        
        self.assertEqual(len(result), 0)

    def test_update_reliability_success(self) -> None:
        """Test successful reliability update."""
        self.supplier_repository.get.return_value = self.supplier
        
        result = self.supplier_service.update_reliability(1, 0.95)
        
        self.assertTrue(result)
        self.supplier_repository.get.assert_called_once_with(1)
        self.supplier_repository.update.assert_called_once()
        
        # Check the updated supplier passed to repository
        updated_supplier = self.supplier_repository.update.call_args[0][0]
        self.assertEqual(updated_supplier.reliability_score, 0.95)
        self.assertEqual(updated_supplier.supplier_id, 1)

    def test_update_reliability_supplier_not_found(self) -> None:
        """Test updating reliability for non-existent supplier."""
        self.supplier_repository.get.return_value = None
        
        result = self.supplier_service.update_reliability(999, 0.95)
        
        self.assertFalse(result)
        self.supplier_repository.update.assert_not_called()

    def test_get_all_suppliers(self) -> None:
        """Test getting all suppliers."""
        mock_suppliers = {
            1: self.supplier,
            2: Mock()
        }
        
        self.supplier_repository.get_all.return_value = mock_suppliers
        
        result = self.supplier_service.get_all_suppliers()
        
        self.assertEqual(result, mock_suppliers)
        self.supplier_repository.get_all.assert_called_once()

    def test_notify_reorder_success(self) -> None:
        """Test successful reorder notification."""
        self.supplier_repository.get.return_value = self.supplier
        
        result = self.supplier_service.notify_reorder(
            "Test Product", 1, 5
        )
        
        self.assertTrue(result)
        self.supplier_repository.get.assert_called_once_with(1)

    def test_notify_reorder_supplier_not_found(self) -> None:
        """Test reorder notification for non-existent supplier."""
        self.supplier_repository.get.return_value = None
        
        result = self.supplier_service.notify_reorder(
            "Test Product", 999, 5
        )
        
        self.assertFalse(result)

    def test_update_reliability_boundary_values(self) -> None:
        """Test updating reliability with boundary values."""
        self.supplier_repository.get.return_value = self.supplier
        
        # Test minimum value
        result1 = self.supplier_service.update_reliability(1, 0.0)
        self.assertTrue(result1)
        
        # Test maximum value
        result2 = self.supplier_service.update_reliability(1, 1.0)
        self.assertTrue(result2)
        
        self.assertEqual(self.supplier_repository.update.call_count, 2)

    def test_get_reliable_suppliers_exact_threshold(self) -> None:
        """Test getting suppliers with reliability exactly at threshold."""
        exact_threshold_supplier = Supplier(
            supplier_id=7,
            name="Exact Threshold Supplier",
            email="exact@test.com",
            reliability_score=0.7  # Exactly at default threshold
        )
        
        self.supplier_repository.get_all.return_value = {
            7: exact_threshold_supplier
        }
        
        result = self.supplier_service.get_reliable_suppliers()
        
        self.assertEqual(len(result), 1)  # Should include supplier with exact threshold


if __name__ == '__main__':
    unittest.main()
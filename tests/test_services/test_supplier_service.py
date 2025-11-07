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

    def setUp(self):
        """Set up test dependencies."""
        self.supplier_repository = Mock()
        self.supplier_service = SupplierService(self.supplier_repository)

        # Create mock supplier
        self.supplier = Supplier(
            supplier_id="sup_001",
            name="Test Supplier",
            email="supplier@test.com",
            reliability_score=0.85
        )

    def test_add_supplier(self):
        """Test adding a new supplier."""
        result = self.supplier_service.add_supplier(
            "sup_002",
            "New Supplier",
            "new@supplier.com",
            0.75
        )

        self.assertIsInstance(result, Supplier)
        self.assertEqual(result.supplier_id, "sup_002")
        self.assertEqual(result.name, "New Supplier")
        self.assertEqual(result.email.value, "new@supplier.com")
        self.assertEqual(result.reliability_score, 0.75)
        
        self.supplier_repository.add.assert_called_once_with(result)

    def test_get_supplier_found(self):
        """Test getting an existing supplier."""
        self.supplier_repository.get.return_value = self.supplier
        
        result = self.supplier_service.get_supplier("sup_001")
        
        self.assertEqual(result, self.supplier)
        self.supplier_repository.get.assert_called_once_with("sup_001")

    def test_get_supplier_not_found(self):
        """Test getting a non-existent supplier."""
        self.supplier_repository.get.return_value = None
        
        result = self.supplier_service.get_supplier("nonexistent")
        
        self.assertIsNone(result)

    def test_get_reliable_suppliers_default_threshold(self):
        """Test getting reliable suppliers with default threshold."""
        reliable_supplier = Supplier(
            supplier_id="reliable_001",
            name="Reliable Supplier",
            email="reliable@test.com",
            reliability_score=0.9
        )
        
        unreliable_supplier = Supplier(
            supplier_id="unreliable_001",
            name="Unreliable Supplier",
            email="unreliable@test.com",
            reliability_score=0.5
        )
        
        self.supplier_repository.get_all.return_value = {
            "reliable_001": reliable_supplier,
            "unreliable_001": unreliable_supplier,
            "sup_001": self.supplier  # 0.85 reliability
        }
        
        result = self.supplier_service.get_reliable_suppliers()
        
        self.assertEqual(len(result), 2)  # Only suppliers with >= 0.7 reliability
        supplier_ids = [s.supplier_id for s in result]
        self.assertIn("reliable_001", supplier_ids)
        self.assertIn("sup_001", supplier_ids)
        self.assertNotIn("unreliable_001", supplier_ids)

    def test_get_reliable_suppliers_custom_threshold(self):
        """Test getting reliable suppliers with custom threshold."""
        supplier1 = Supplier(
            supplier_id="sup1",
            name="Supplier 1",
            email="sup1@test.com",
            reliability_score=0.6
        )
        
        supplier2 = Supplier(
            supplier_id="sup2",
            name="Supplier 2",
            email="sup2@test.com",
            reliability_score=0.8
        )
        
        self.supplier_repository.get_all.return_value = {
            "sup1": supplier1,
            "sup2": supplier2,
            "sup_001": self.supplier  # 0.85 reliability
        }
        
        # Test with threshold of 0.75
        result = self.supplier_service.get_reliable_suppliers(0.75)
        
        self.assertEqual(len(result), 2)  # Only suppliers with >= 0.75 reliability
        supplier_ids = [s.supplier_id for s in result]
        self.assertIn("sup2", supplier_ids)
        self.assertIn("sup_001", supplier_ids)
        self.assertNotIn("sup1", supplier_ids)

    def test_get_reliable_suppliers_none_meet_threshold(self):
        """Test getting reliable suppliers when none meet threshold."""
        unreliable_supplier = Supplier(
            supplier_id="unreliable_001",
            name="Unreliable Supplier",
            email="unreliable@test.com",
            reliability_score=0.3
        )
        
        self.supplier_repository.get_all.return_value = {
            "unreliable_001": unreliable_supplier
        }
        
        result = self.supplier_service.get_reliable_suppliers(0.8)
        
        self.assertEqual(len(result), 0)

    def test_update_reliability_success(self):
        """Test successful reliability update."""
        self.supplier_repository.get.return_value = self.supplier
        
        result = self.supplier_service.update_reliability("sup_001", 0.95)
        
        self.assertTrue(result)
        self.supplier_repository.get.assert_called_once_with("sup_001")
        self.supplier_repository.update.assert_called_once()
        
        # Check the updated supplier passed to repository
        updated_supplier = self.supplier_repository.update.call_args[0][0]
        self.assertEqual(updated_supplier.reliability_score, 0.95)
        self.assertEqual(updated_supplier.supplier_id, "sup_001")

    def test_update_reliability_supplier_not_found(self):
        """Test updating reliability for non-existent supplier."""
        self.supplier_repository.get.return_value = None
        
        result = self.supplier_service.update_reliability("nonexistent", 0.95)
        
        self.assertFalse(result)
        self.supplier_repository.update.assert_not_called()

    def test_get_all_suppliers(self):
        """Test getting all suppliers."""
        mock_suppliers = {
            "sup_001": self.supplier,
            "sup_002": Mock()
        }
        
        self.supplier_repository.get_all.return_value = mock_suppliers
        
        result = self.supplier_service.get_all_suppliers()
        
        self.assertEqual(result, mock_suppliers)
        self.supplier_repository.get_all.assert_called_once()

    def test_notify_reorder_success(self):
        """Test successful reorder notification."""
        self.supplier_repository.get.return_value = self.supplier
        
        result = self.supplier_service.notify_reorder(
            "Test Product", "sup_001", 5
        )
        
        self.assertTrue(result)
        self.supplier_repository.get.assert_called_once_with("sup_001")

    def test_notify_reorder_supplier_not_found(self):
        """Test reorder notification for non-existent supplier."""
        self.supplier_repository.get.return_value = None
        
        result = self.supplier_service.notify_reorder(
            "Test Product", "nonexistent", 5
        )
        
        self.assertFalse(result)

    def test_update_reliability_boundary_values(self):
        """Test updating reliability with boundary values."""
        self.supplier_repository.get.return_value = self.supplier
        
        # Test minimum value
        result1 = self.supplier_service.update_reliability("sup_001", 0.0)
        self.assertTrue(result1)
        
        # Test maximum value
        result2 = self.supplier_service.update_reliability("sup_001", 1.0)
        self.assertTrue(result2)
        
        self.assertEqual(self.supplier_repository.update.call_count, 2)

    def test_get_reliable_suppliers_exact_threshold(self):
        """Test getting suppliers with reliability exactly at threshold."""
        exact_threshold_supplier = Supplier(
            supplier_id="exact_001",
            name="Exact Threshold Supplier",
            email="exact@test.com",
            reliability_score=0.7  # Exactly at default threshold
        )
        
        self.supplier_repository.get_all.return_value = {
            "exact_001": exact_threshold_supplier
        }
        
        result = self.supplier_service.get_reliable_suppliers()
        
        self.assertEqual(len(result), 1)  # Should include supplier with exact threshold


if __name__ == '__main__':
    unittest.main()
"""
Test SalesReport value object - validation and immutability
Tests sales report creation and data integrity
"""
import unittest
from domain.value_objects.sales_report import SalesReport


class TestSalesReport(unittest.TestCase):
    """Test SalesReport value object."""

    def test_sales_report_creation_valid(self) -> None:
        """Test creating SalesReport with valid data."""
        report = SalesReport(
            total_sales=1000.0,
            total_orders=10,
            cancelled_orders=2,
            products_sold={1: 5, 2: 3},
            revenue_by_category={"Electronics": 800.0, "Books": 200.0},
            top_customers=[(101, 500.0), (102, 300.0)]
        )
        
        self.assertEqual(report.total_sales, 1000.0)
        self.assertEqual(report.total_orders, 10)
        self.assertEqual(report.cancelled_orders, 2)
        self.assertEqual(report.products_sold, {1: 5, 2: 3})
        self.assertEqual(report.revenue_by_category, {"Electronics": 800.0, "Books": 200.0})
        self.assertEqual(report.top_customers, [(101, 500.0), (102, 300.0)])

    def test_negative_total_sales(self) -> None:
        """Test validation for negative total sales."""
        with self.assertRaises(ValueError) as context:
            SalesReport(
                total_sales=-100.0,  # Invalid
                total_orders=5,
                cancelled_orders=0,
                products_sold={},
                revenue_by_category={},
                top_customers=[]
            )
        self.assertIn("Total sales cannot be negative", str(context.exception))

    def test_negative_total_orders(self) -> None:
        """Test validation for negative total orders."""
        with self.assertRaises(ValueError) as context:
            SalesReport(
                total_sales=100.0,
                total_orders=-5,  # Invalid
                cancelled_orders=0,
                products_sold={},
                revenue_by_category={},
                top_customers=[]
            )
        self.assertIn("Total orders cannot be negative", str(context.exception))

    def test_negative_cancelled_orders(self) -> None:
        """Test validation for negative cancelled orders."""
        with self.assertRaises(ValueError) as context:
            SalesReport(
                total_sales=100.0,
                total_orders=5,
                cancelled_orders=-2,  # Invalid
                products_sold={},
                revenue_by_category={},
                top_customers=[]
            )
        self.assertIn("Cancelled orders cannot be negative", str(context.exception))

    def test_immutability_defensive_copies(self) -> None:
        """Test that returned collections are defensive copies."""
        original_products = {1: 5, 2: 3}
        original_revenue = {"Electronics": 800.0}
        original_customers = [(101, 500.0)]
        
        report = SalesReport(
            total_sales=1000.0,
            total_orders=10,
            cancelled_orders=2,
            products_sold=original_products,
            revenue_by_category=original_revenue,
            top_customers=original_customers
        )
        
        # Modify returned collections
        products_copy = report.products_sold
        revenue_copy = report.revenue_by_category
        customers_copy = report.top_customers
        
        products_copy[3] = 10  # Should not affect original
        revenue_copy["Books"] = 200.0
        customers_copy.append((103, 100.0))
        
        # Verify original data is unchanged
        self.assertEqual(report.products_sold, {1: 5, 2: 3})
        self.assertEqual(report.revenue_by_category, {"Electronics": 800.0})
        self.assertEqual(report.top_customers, [(101, 500.0)])

    def test_to_dict(self) -> None:
        """Test converting report to dictionary."""
        report = SalesReport(
            total_sales=1000.0,
            total_orders=10,
            cancelled_orders=2,
            products_sold={1: 5, 2: 3},
            revenue_by_category={"Electronics": 800.0, "Books": 200.0},
            top_customers=[(101, 500.0), (102, 300.0)]
        )
        
        result = report.to_dict()
        expected = {
            'total_sales': 1000.0,
            'total_orders': 10,
            'cancelled_orders': 2,
            'products_sold': {1: 5, 2: 3},
            'revenue_by_category': {"Electronics": 800.0, "Books": 200.0},
            'top_customers': [(101, 500.0), (102, 300.0)]
        }
        
        self.assertEqual(result, expected)

    def test_string_representations(self) -> None:
        """Test string representations of report."""
        report = SalesReport(
            total_sales=1000.0,
            total_orders=10,
            cancelled_orders=2,
            products_sold={},
            revenue_by_category={},
            top_customers=[]
        )
        
        str_repr = str(report)
        self.assertIn("$1000.00", str_repr)
        self.assertIn("10 orders", str_repr)
        self.assertIn("2 cancelled", str_repr)
        
        repr_str = repr(report)
        self.assertIn("SalesReport", repr_str)
        self.assertIn("total_sales=1000.0", repr_str)

    def test_equality(self) -> None:
        """Test report equality comparison."""
        report1 = SalesReport(
            total_sales=1000.0,
            total_orders=10,
            cancelled_orders=2,
            products_sold={1: 5},
            revenue_by_category={"Electronics": 800.0},
            top_customers=[(101, 500.0)]
        )
        
        report2 = SalesReport(
            total_sales=1000.0,
            total_orders=10,
            cancelled_orders=2,
            products_sold={1: 5},
            revenue_by_category={"Electronics": 800.0},
            top_customers=[(101, 500.0)]
        )
        
        self.assertEqual(report1, report2)

    def test_inequality_different_sales(self) -> None:
        """Test report inequality with different total sales."""
        report1 = SalesReport(
            total_sales=1000.0,
            total_orders=10,
            cancelled_orders=2,
            products_sold={},
            revenue_by_category={},
            top_customers=[]
        )
        
        report2 = SalesReport(
            total_sales=2000.0,  # Different
            total_orders=10,
            cancelled_orders=2,
            products_sold={},
            revenue_by_category={},
            top_customers=[]
        )
        
        self.assertNotEqual(report1, report2)

    def test_hash_functionality(self) -> None:
        """Test that reports can be used in sets/dicts."""
        report = SalesReport(
            total_sales=1000.0,
            total_orders=10,
            cancelled_orders=2,
            products_sold={1: 5},
            revenue_by_category={"Electronics": 800.0},
            top_customers=[(101, 500.0)]
        )
        
        # Should be able to hash (for sets/dicts)
        report_set = {report}
        self.assertIn(report, report_set)

    def test_empty_report(self) -> None:
        """Test creating empty sales report."""
        report = SalesReport(
            total_sales=0.0,
            total_orders=0,
            cancelled_orders=0,
            products_sold={},
            revenue_by_category={},
            top_customers=[]
        )
        
        self.assertEqual(report.total_sales, 0.0)
        self.assertEqual(report.total_orders, 0)
        self.assertEqual(report.cancelled_orders, 0)
        self.assertEqual(len(report.products_sold), 0)
        self.assertEqual(len(report.revenue_by_category), 0)
        self.assertEqual(len(report.top_customers), 0)


if __name__ == '__main__':
    unittest.main()
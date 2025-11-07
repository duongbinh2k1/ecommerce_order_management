"""
Test PromotionService - promotional campaign management
Tests promotion creation, validation, and usage tracking
"""
import unittest
from unittest.mock import Mock
from datetime import datetime, timedelta
from services.promotion_service import PromotionService
from domain.models.promotion import Promotion


class TestPromotionService(unittest.TestCase):
    """Test PromotionService promotion management functionality."""

    def setUp(self):
        """Set up test dependencies."""
        self.promotion_repository = Mock()
        self.promotion_service = PromotionService(self.promotion_repository)

        # Create mock promotion
        future_date = datetime.now() + timedelta(days=30)
        self.promotion = Promotion(
            promo_id="promo_001",
            code="SAVE20",
            discount_percent=20.0,
            min_purchase=100.0,
            valid_until=future_date,
            category="all"
        )

    def test_add_promotion(self):
        """Test adding a new promotion."""
        future_date = datetime.now() + timedelta(days=15)
        
        result = self.promotion_service.add_promotion(
            "promo_002",
            "NEWUSER10",
            10.0,
            50.0,
            future_date,
            "electronics"
        )

        self.assertIsInstance(result, Promotion)
        self.assertEqual(result.promo_id, "promo_002")
        self.assertEqual(result.code, "NEWUSER10")
        self.assertEqual(result.discount_percent, 10.0)
        self.assertEqual(result.min_purchase, 50.0)
        self.assertEqual(result.valid_until, future_date)
        self.assertEqual(result.category, "electronics")
        
        self.promotion_repository.add.assert_called_once_with(result)

    def test_get_promotion_valid(self):
        """Test getting a valid promotion."""
        self.promotion_repository.get.return_value = self.promotion
        
        result = self.promotion_service.get_promotion("SAVE20")
        
        self.assertEqual(result, self.promotion)
        self.promotion_repository.get.assert_called_once_with("SAVE20")

    def test_get_promotion_expired(self):
        """Test getting an expired promotion."""
        # Create expired promotion
        past_date = datetime.now() - timedelta(days=5)
        expired_promotion = Promotion(
            promo_id="promo_expired",
            code="EXPIRED",
            discount_percent=15.0,
            min_purchase=75.0,
            valid_until=past_date,
            category="all"
        )
        
        self.promotion_repository.get.return_value = expired_promotion
        
        result = self.promotion_service.get_promotion("EXPIRED")
        
        self.assertIsNone(result)

    def test_get_promotion_not_found(self):
        """Test getting a non-existent promotion."""
        self.promotion_repository.get.return_value = None
        
        result = self.promotion_service.get_promotion("NOTEXIST")
        
        self.assertIsNone(result)

    def test_increment_usage_success(self):
        """Test incrementing promotion usage count."""
        self.promotion_repository.get.return_value = self.promotion
        initial_count = self.promotion.used_count
        
        result = self.promotion_service.increment_usage("SAVE20")
        
        self.assertTrue(result)
        self.assertEqual(self.promotion.used_count, initial_count + 1)

    def test_increment_usage_promotion_not_found(self):
        """Test incrementing usage for non-existent promotion."""
        self.promotion_repository.get.return_value = None
        
        result = self.promotion_service.increment_usage("NOTEXIST")
        
        self.assertFalse(result)

    def test_get_active_promotions(self):
        """Test getting all active promotions."""
        # Create active and expired promotions
        future_date = datetime.now() + timedelta(days=10)
        past_date = datetime.now() - timedelta(days=5)
        
        active_promo = Promotion(
            promo_id="active_001",
            code="ACTIVE",
            discount_percent=25.0,
            min_purchase=100.0,
            valid_until=future_date,
            category="all"
        )
        
        expired_promo = Promotion(
            promo_id="expired_001",
            code="EXPIRED",
            discount_percent=15.0,
            min_purchase=50.0,
            valid_until=past_date,
            category="all"
        )
        
        self.promotion_repository.get_all.return_value = {
            "ACTIVE": active_promo,
            "EXPIRED": expired_promo,
            "SAVE20": self.promotion
        }
        
        active_promos = self.promotion_service.get_active_promotions()
        
        self.assertEqual(len(active_promos), 2)  # Only active ones
        active_codes = [promo.code for promo in active_promos]
        self.assertIn("ACTIVE", active_codes)
        self.assertIn("SAVE20", active_codes)
        self.assertNotIn("EXPIRED", active_codes)

    def test_get_active_promotions_none_active(self):
        """Test getting active promotions when none are active."""
        past_date = datetime.now() - timedelta(days=5)
        
        expired_promo = Promotion(
            promo_id="expired_001",
            code="EXPIRED",
            discount_percent=15.0,
            min_purchase=50.0,
            valid_until=past_date,
            category="all"
        )
        
        self.promotion_repository.get_all.return_value = {
            "EXPIRED": expired_promo
        }
        
        active_promos = self.promotion_service.get_active_promotions()
        
        self.assertEqual(len(active_promos), 0)

    def test_get_all_promotions(self):
        """Test getting all promotions."""
        mock_promotions = {
            "SAVE20": self.promotion,
            "TEST": Mock()
        }
        
        self.promotion_repository.get_all.return_value = mock_promotions
        
        result = self.promotion_service.get_all_promotions()
        
        self.assertEqual(result, mock_promotions)
        self.promotion_repository.get_all.assert_called_once()

    def test_get_promotion_just_expired(self):
        """Test getting a promotion that just expired."""
        # Create promotion that expires right now
        now = datetime.now()
        just_expired_promotion = Promotion(
            promo_id="just_expired",
            code="JUSTEXPIRED",
            discount_percent=30.0,
            min_purchase=200.0,
            valid_until=now - timedelta(microseconds=1),  # Just expired
            category="all"
        )
        
        self.promotion_repository.get.return_value = just_expired_promotion
        
        result = self.promotion_service.get_promotion("JUSTEXPIRED")
        
        self.assertIsNone(result)

    def test_multiple_usage_increments(self):
        """Test incrementing usage multiple times."""
        self.promotion_repository.get.return_value = self.promotion
        initial_count = self.promotion.used_count
        
        # Increment multiple times
        self.promotion_service.increment_usage("SAVE20")
        self.promotion_service.increment_usage("SAVE20")
        self.promotion_service.increment_usage("SAVE20")
        
        self.assertEqual(self.promotion.used_count, initial_count + 3)


if __name__ == '__main__':
    unittest.main()
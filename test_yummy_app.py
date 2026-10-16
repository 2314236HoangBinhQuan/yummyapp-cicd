import unittest
from unittest.mock import patch

import gps_service
from yummy_app import YummyApp


class TestEasyLevel(unittest.TestCase):
    """Kiem thu chuc nang co ban tinh tien don hang."""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)


# ======================================================================
# CAP DO 2 (TIET 3): SINH VIEN TU TAY LAP TRINH TEST CASE DUOI DAY
# (Sau khi da hoan thanh Ban thiet ke test case viet tay tren giay)
# ======================================================================

class TestMediumLevel(unittest.TestCase):
    """Kiem thu ap dung ma khuyen mai."""

    def test_apply_promo_code_online_valid(self):
        app = YummyApp(network_status="online")
        self.assertEqual(app.apply_promo_code(100000, "GIAM10"), 90000)

    def test_apply_promo_code_offline_raises_connection_error(self):
        app = YummyApp(network_status="offline")
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_apply_new_os_only_on_os_15(self):
        app = YummyApp(os_version=15)
        self.assertEqual(app.apply_promo_code(100000, "NEW_OS_ONLY"), 80000)

    def test_apply_new_os_only_on_os_14_raises_value_error(self):
        app = YummyApp(os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")


class TestHardLevel(unittest.TestCase):
    """Kiem thu de xuat nha hang voi dich vu GPS duoc mock."""

    def setUp(self):
        self.app = YummyApp()

    @patch("yummy_app.gps_service.get_current_location")
    def test_get_nearby_restaurants_in_supported_location(self, mock_location):
        mock_location.return_value = (10.0, 105.0)
        expected = ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"]
        self.assertEqual(self.app.get_nearby_restaurants(), expected)

    @patch("yummy_app.gps_service.get_current_location")
    def test_get_nearby_restaurants_outside_supported_location(self, mock_location):
        mock_location.return_value = (20.0, 110.0)
        self.assertEqual(self.app.get_nearby_restaurants(), [])

    @patch("yummy_app.gps_service.get_current_location")
    def test_get_nearby_restaurants_when_gps_signal_is_lost(self, mock_location):
        mock_location.side_effect = gps_service.GPSSignalLostError
        self.assertEqual(
            self.app.get_nearby_restaurants(), "Khong the xac dinh vi tri."
        )


if __name__ == "__main__":
    unittest.main()

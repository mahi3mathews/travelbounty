import unittest
from app.commission import Commission


class TestCommission(unittest.TestCase):

    def test_set_commission_amount(self):
        b = Commission()
        b.set_amount(120)
        self.assertEqual(120, b.get_amount())

    def test_set_commission_created_details(self):
        b = Commission()
        b.set_created_by({
            "admin_id": "admin1"
        })
        self.assertEqual("admin1", b.get_created_by()["admin_id"])


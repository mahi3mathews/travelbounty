import unittest
from app.travel_service import TravelService
from enums.service_types import ServiceTypes


class TestTravelService(unittest.TestCase):

    def test_set_service_name(self):
        b = TravelService()
        b.set_name("AirAsia")
        self.assertNotEqual(b.get_name(), "Emirates")
        self.assertEqual(b.get_name(), "AirAsia")

    def test_set_service_details(self):
        b = TravelService()
        b.set_name("AirAsia")
        b.set_type(ServiceTypes.FLIGHT)
        b.set_price(100)
        b.set_details({"start_loc": "Tokyo", "final_loc": "Seoul", "flight": "AS183"})
        self.assertEqual(b.get_price(), 100)
        self.assertEqual(b.get_details(), {"start_loc": "Tokyo", "final_loc": "Seoul", "flight": "AS183"})
        self.assertEqual(b.get_type(), ServiceTypes.FLIGHT)

import unittest
from app.itinerary import Itinerary

from tests.sample_data.itineraries import itineraries
from tests.sample_data.travel_services import travel_services


class TestItinerary(unittest.TestCase):

    def test_set_itinerary_id(self):
        b = Itinerary("agentId1")
        b.set_itinerary_id("i123")
        self.assertEqual(b.get_itinerary_id(), "i123")

    def test_set_agent_id(self):
        b = Itinerary("a_id1")
        self.assertEqual(b.get_agent(), "a_id1")

    def test_itinerary_total_price(self):
        b = Itinerary("a_id1")
        b.set_travel_services(itineraries()[0]["services"])
        b.set_services(travel_services())
        b.set_total_price(b.calculate_total_sales(b.get_travel_services()))
        self.assertEqual(1400, b.get_total_price())

    def test_itinerary_total_commission(self):
        b = Itinerary("a_id1")
        b.set_travel_services(itineraries()[0]["services"])
        b.set_services(travel_services())
        b.set_travel_service_commission(b.calculate_sale_commission(b.get_travel_services()))
        self.assertEqual(215, b.get_travel_service_commission())



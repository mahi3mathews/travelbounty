import unittest
from app.service_factory import ServiceFactory


class TestAgentServiceFactory(unittest.TestCase):

    def test_set_agent_id(self):
        b = ServiceFactory("agent_id1")
        self.assertEqual(b.get_agent_id(), "agent_id1")

    def test_get_admin_service_booking(self):
        b = ServiceFactory("a_id1")
        service = b.get_service("booking")
        service.set_total_price(100)
        self.assertEqual(100, service.get_total_price())

    def test_get_admin_service_itinerary(self):
        b = ServiceFactory("a_id1")
        service = b.get_service("itinerary")
        service.set_name("Name")
        self.assertEqual("Name", service.get_name())









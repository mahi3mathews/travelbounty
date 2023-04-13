import unittest
from app.services import Services
from tests.sample_data.travel_services import travel_services
from tests.sample_data.bookings import bookings
from tests.sample_data.users import users


class TestServicesMediator(unittest.TestCase):

    def test_total_commission(self):
        b = Services()
        b.set_services(travel_services())
        b.set_bookings(bookings())
        total_commission = b.calculate_all_services_commission()
        expected_total_commission = {'641eb28b48472e33df53441c': 39.0,
                                     '641eb2953d0171e92a395dc2': 13.0,
                                     '641eb29c9b2f3a0cbaa4ee34': 720.0,
                                     '641eb2a788d9a053e4054a4e': 40.0}
        self.assertEqual(total_commission, expected_total_commission)

    def test_calculate_all_services_sale(self):
        b = Services()
        b.set_services(travel_services())
        b.set_bookings(bookings())
        total_sales = b.calculate_all_services_sale()
        expected_total_sales = {'641eb28b48472e33df53441c': 280.0,
                                '641eb2953d0171e92a395dc2': 260.0,
                                '641eb29c9b2f3a0cbaa4ee34': 3600.0,
                                '641eb2a788d9a053e4054a4e': 400.0}
        self.assertEqual(total_sales, expected_total_sales)

    def test_calculate_sale_by_agents(self):
        b = Services()
        b.set_services(travel_services())
        b.set_bookings(bookings())
        agents = [users()[0], users()[1], users()[2]]
        total_agent_sales = b.calculate_sale_by_agent(agents)
        expected_total_sales = [{'Seline Cooper': {'641eb28b48472e33df53441c': 140.0,
                                                   '641eb2953d0171e92a395dc2': 260.0,
                                                   '641eb29c9b2f3a0cbaa4ee34': 2400.0,
                                                   '641eb2a788d9a053e4054a4e': 200.0}},
                                {'Talia K': {'641eb28b48472e33df53441c': 140.0,
                                             '641eb29c9b2f3a0cbaa4ee34': 1200.0,
                                             '641eb2a788d9a053e4054a4e': 200.0}}]
        self.assertEqual(expected_total_sales, total_agent_sales)

    def test_calculate_total_sales(self):
        b = Services()
        b.set_services(travel_services())
        b.set_bookings(bookings())
        service_sales = [travel_services()[0]["_id"], travel_services()[1]["_id"], travel_services()[2]["_id"]]
        total_service_sales = b.calculate_total_sales(service_sales)
        expected_total_service_sales = 2300
        self.assertEqual(expected_total_service_sales, total_service_sales)

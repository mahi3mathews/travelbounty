import unittest
from app.booking import Booking
from tests.sample_data.travel_services import travel_services
from tests.sample_data.bookings import bookings


class TestBooking(unittest.TestCase):

    def test_set_booking_id(self):
        b = Booking("a_id1")
        b.set_booking_id("bookingId1")
        self.assertEqual(b.get_booking_id(), "bookingId1")

    def test_set_agent_id(self):
        b = Booking("a_id1")
        b.set_agent_id("a_id2")
        self.assertEqual(b.get_agent_id(), "a_id2")

    def test_booking_total_price(self):
        b = Booking("a_id1")
        b.set_services(travel_services())
        b.set_total_price(b.calculate_total_sales(bookings()[1]["services"]))
        self.assertNotEqual(1461, b.get_total_price())
        self.assertEqual(1460, b.get_total_price())

    def test_booking_total_price(self):
        b = Booking("a_id1")
        b.set_services(travel_services())
        b.set_total_price(b.calculate_total_sales(bookings()[1]["services"]))
        self.assertNotEqual(1461, b.get_total_price())
        self.assertEqual(1470, b.get_total_price())

    def test_booking_total_commission(self):
        b = Booking("a_id3")
        b.set_services(travel_services())
        b.set_agent_commissions(b.calculate_sale_commission(bookings()[1]["services"]))
        self.assertEqual(266, b.get_agent_commissions())





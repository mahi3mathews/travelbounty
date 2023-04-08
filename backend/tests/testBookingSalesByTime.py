import unittest
from datetime import datetime, time, timedelta, date
from app.booking_sales_by_time import BookingSalesByTime
from tests.sample_data.bookings import bookings


class TestBookingSalesByTime(unittest.TestCase):

    def test_set_booking_sales_daily_filter(self):
        b = BookingSalesByTime()
        now = datetime.now()
        start_time = datetime.combine(now.date(), time(hour=8))
        end_time = datetime.combine(now.date(), time(hour=18))
        expected_result = {"booking_date": {"$gte": start_time, "$lt": end_time}}
        daily_filter = b.get_daily_filter("booking_date")

        self.assertIn("booking_date", daily_filter)
        self.assertIsInstance(daily_filter["booking_date"], dict)
        self.assertDictEqual(expected_result, daily_filter)

    def test_set_booking_sales_daily_sales(self):
        b = BookingSalesByTime()
        booking_time_1 = time(hour=10, minute=20, second=0)
        booking_time_2 = time(hour=13, minute=0, second=0)
        booking_time_3 = time(hour=18, minute=45, second=0)
        bookings_list = bookings()
        bookings_list[0]["created_on"] = datetime.combine(datetime.now(), booking_time_1)
        bookings_list[1]["created_on"] = datetime.combine(datetime.now(), booking_time_2)
        bookings_list[2]["created_on"] = datetime.combine(datetime.now(), booking_time_3)
        expected_result = [{"8am": 0}, {"9am": 0}, {"10am": 100}, {"11am": 0}, {"12pm": 0}, {"1pm": 600}, {"2pm": 0},
                           {"3pm": 0}, {"4pm": 0}, {"5pm": 0}, {"6pm": 200}]
        daily_sales = b.get_daily_sales(bookings_list)
        self.assertEqual(len(expected_result), len(daily_sales))
        self.assertListEqual(expected_result, daily_sales)

    def test_set_booking_sales_weekly_filter(self):
        b = BookingSalesByTime()
        today = date.today()
        sat_offset = (today.weekday() - 5) % 7
        fri_offset = (4 - today.weekday()) % 7
        start_date = today - timedelta(days=sat_offset)
        end_date = today + timedelta(days=fri_offset)
        expected_result = {"booking_date": {"$gte": datetime.combine(start_date, datetime.min.time()),
                                            "$lt": datetime.combine(end_date, datetime.min.time())}}
        weekly_filter = b.get_weekly_filter("booking_date")

        self.assertIn("booking_date", weekly_filter)
        self.assertIsInstance(weekly_filter["booking_date"], dict)
        self.assertDictEqual(expected_result, weekly_filter)

    def test_set_booking_sales_weekly_sales(self):
        b = BookingSalesByTime()
        today = date.today()
        sat_offset = (today.weekday() - 5) % 7
        start_date = today - timedelta(days=sat_offset)
        booking_time_1 = datetime.combine(start_date + timedelta(days=1), time(0, 0, 0))
        booking_time_2 = datetime.combine(start_date + timedelta(days=3), time(0, 0, 0))
        booking_time_3 = datetime.combine(start_date + timedelta(days=5), time(0, 0, 0))
        bookings_list = bookings()
        bookings_list[0]["created_on"] = booking_time_1
        bookings_list[1]["created_on"] = booking_time_2
        bookings_list[2]["created_on"] = booking_time_3
        expected_result = [{"Mon": 0}, {"Tue": 600}, {"Wed": 0}, {"Thu": 200}, {"Fri": 0}, {"Sat": 0}, {"Sun": 100}]
        daily_sales = b.get_weekly_sales(bookings_list)
        self.assertEqual(len(expected_result), len(daily_sales))
        self.assertListEqual(expected_result, daily_sales)

    def test_set_booking_sales_monthly_filter(self):
        b = BookingSalesByTime()
        current_year = datetime.now().year
        start_date = datetime(current_year, 1, 1)
        end_date = datetime(current_year, 12, 31)
        expected_result = {"booking_date": {"$gte": start_date, "$lte": end_date}}
        monthly_filter = b.get_monthly_filter("booking_date")

        self.assertIn("booking_date", monthly_filter)
        self.assertIsInstance(monthly_filter["booking_date"], dict)
        self.assertDictEqual(expected_result, monthly_filter)

    def test_set_booking_sales_monthly_sales(self):
        b = BookingSalesByTime()
        current_year = datetime.now().year
        booking_time_1 = datetime(current_year, 2, 18)
        booking_time_2 = datetime(current_year, 6, 30)
        booking_time_3 = datetime(current_year, 9, 19)
        bookings_list = bookings()
        bookings_list[0]["created_on"] = booking_time_1
        bookings_list[1]["created_on"] = booking_time_2
        bookings_list[2]["created_on"] = booking_time_3
        expected_result = [{"Jan": 0}, {"Feb": 100}, {"Mar": 0}, {"Apr": 0}, {"May": 0}, {"Jun": 600}, {"Jul": 0},
                           {"Aug": 0}, {"Sep": 200}, {"Oct": 0}, {"Nov": 0}, {"Dec": 0}]

        monthly_sales = b.get_monthly_sales(bookings_list)
        self.assertEqual(len(expected_result), len(monthly_sales))
        self.assertListEqual(expected_result, monthly_sales)

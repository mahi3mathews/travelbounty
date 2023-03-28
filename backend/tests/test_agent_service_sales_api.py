import unittest
from unittest import mock
from unittest.mock import MagicMock
from flask import current_app, jsonify
from datetime import datetime, time, date, timedelta
from flask_pymongo import ObjectId
from enums.payment_status import PaymentStatus
from enums.roles import Roles
from app.main import app
from app.service_sales import ServiceSales
from app.daily_sales import DailySales
from app.weekly_sales import WeeklySales
from app.monthly_sales import MonthlySales

from schemas.itinerary import itinerary_entity, itinerary_list_entity
from schemas.booking import booking_entity, booking_list_entity
from schemas.services import service_list_entity
from tests.sample_data.travel_services import travel_services
from tests.sample_data.bookings import bookings
from tests.sample_data.users import users
from tests.sample_data.itineraries import itineraries

from api_functions.agent_service_sales_api import fetch_service_sales, fetch_agent_service_commissions, \
    fetch_agents_booking_sales, fetch_agent_total_price_bookings_timely, fetch_total_price_bookings_timely


class TestAgentServiceSales(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.mock_db = MagicMock()
        with self.app.app_context():
            current_app._get_current_object = lambda: app

    def test_admin_fetch_service_sales(self):
        request_data = {
            "u_id": str(users()[3]["_id"])
        }
        mock_services_collection = MagicMock()
        mock_services_collection.find.return_value = travel_services()
        mock_users_collection = MagicMock()
        mock_users_collection.find.return_value = users()
        mock_users_collection.find_one.return_value = users()[3]
        mock_bookings_collection = MagicMock()
        mock_bookings_collection.find.return_value = bookings()

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "service": mock_services_collection,
            "user": mock_users_collection,
            "booking": mock_bookings_collection
        }.get(x)

        total_sales = ServiceSales.all_services_sale(bookings(), travel_services())

        with self.app.app_context():
            result = fetch_service_sales(request_data, mock_db)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully fetched all services sales.", str(result.data))
        self.assertDictEqual(total_sales, res["data"])
        mock_db["booking"].find.assert_called_once_with()
        mock_db["service"].find.assert_called_once_with()
        mock_db["user"].find_one.assert_called_once_with({"_id": ObjectId(request_data["u_id"])})

    def test_agent_fetch_service_sales(self):
        request_data = {
            "u_id": str(users()[1]["_id"])
        }
        agent_bookings = [bookings()[0], bookings()[1]]
        mock_services_collection = MagicMock()
        mock_services_collection.find.return_value = travel_services()
        mock_users_collection = MagicMock()
        mock_users_collection.find.return_value = users()
        mock_users_collection.find_one.return_value = users()[1]
        mock_bookings_collection = MagicMock()
        mock_bookings_collection.find.return_value = agent_bookings

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "service": mock_services_collection,
            "user": mock_users_collection,
            "booking": mock_bookings_collection
        }.get(x)

        total_sales = ServiceSales.all_services_sale(agent_bookings, travel_services())

        with self.app.app_context():
            result = fetch_service_sales(request_data, mock_db)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully fetched all services sales.", str(result.data))
        self.assertDictEqual(total_sales, res["data"])
        mock_db["booking"].find.assert_called_once_with({"agent_id": request_data["u_id"]})
        mock_db["service"].find.assert_called_once_with()
        mock_db["user"].find_one.assert_called_once_with({"_id": ObjectId(request_data["u_id"])})

    def test_fetch_agent_commissions(self):
        request_data = {
            "agent_id": str(users()[1]["_id"]),
            "is_agent": True
        }
        agent_bookings = [bookings()[0], bookings()[1]]
        mock_services_collection = MagicMock()
        mock_services_collection.find.return_value = travel_services()
        mock_bookings_collection = MagicMock()
        mock_bookings_collection.find.return_value = agent_bookings

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "service": mock_services_collection,
            "booking": mock_bookings_collection
        }.get(x)

        total_commissions = ServiceSales.all_services_commission(agent_bookings, travel_services())

        with self.app.app_context():
            result = fetch_agent_service_commissions(request_data, mock_db)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully fetched all services commissions.", str(result.data))
        self.assertDictEqual(total_commissions, res["data"])
        mock_db["booking"].find.assert_called_once_with({"agent_id": request_data["agent_id"]})
        mock_db["service"].find.assert_called_once_with()

    def test_fetch_agent_commissions_error(self):
        request_data = {
            "agent_id": str(users()[1]["_id"]),
            "is_agent": False
        }
        agent_bookings = [bookings()[0], bookings()[1]]
        mock_services_collection = MagicMock()
        mock_services_collection.find.return_value = travel_services()
        mock_bookings_collection = MagicMock()
        mock_bookings_collection.find.return_value = agent_bookings

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "service": mock_services_collection,
            "booking": mock_bookings_collection
        }.get(x)

        with self.app.app_context():
            result = fetch_agent_service_commissions(request_data, mock_db)
        self.assertEqual(result.status_code, 401)
        self.assertIn("User does not have permission to view service commissions", str(result.data))
        assert mock_db["booking"].find.call_count <= 0
        assert mock_db["service"].find.call_count <= 0

    def test_fetch_agents_booking_sales(self):
        request_data = {
            "is_admin": True,
            "agent_id": str(users()[3]["_id"])
        }
        agent_users = [users()[0], users()[1], users()[2]]
        mock_services_collection = MagicMock()
        mock_services_collection.find.return_value = travel_services()
        mock_users_collection = MagicMock()
        mock_users_collection.find.return_value = agent_users
        mock_booking_collection = MagicMock()
        mock_booking_collection.find.return_value = bookings()

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "service": mock_services_collection,
            "user": mock_users_collection,
            "booking": mock_booking_collection
        }.get(x)
        expected_res = ServiceSales.services_sold(bookings(), travel_services(), agent_users)

        with self.app.app_context():
            result = fetch_agents_booking_sales(request_data, mock_db)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully fetched the services booked by agents.", str(result.data))
        self.assertListEqual(expected_res, res["data"])
        mock_db["booking"].find.assert_called_once_with()
        mock_db["service"].find.assert_called_once_with()
        mock_db["user"].find.assert_called_once_with({"role": Roles.AGENT.value})

    def test_agent_total_price_daily_bookings(self):
        request_data = {
            "agent_id": str(users()[1]["_id"]),
            "is_agent": True,
            "filter": "daily"
        }
        agent_bookings = [bookings()[0], bookings()[1]]
        agent_bookings[0]["booking_date"] = datetime.combine(datetime.now(), time(hour=10, minute=20, second=0))
        agent_bookings[1]["booking_date"] = datetime.combine(datetime.now(), time(hour=13, minute=0, second=0))
        mock_bookings_collection = MagicMock()
        mock_bookings_collection.find.return_value = agent_bookings

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "booking": mock_bookings_collection
        }.get(x)
        expected_query = {
            "$and": [
                {"agent_id": request_data["agent_id"]},
                DailySales().get_filter("booking_date")]
        }
        expected_response = DailySales().calculate_sales(agent_bookings)
        with self.app.app_context():
            result = fetch_agent_total_price_bookings_timely(request_data, mock_db)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully fetched total price of bookings.", str(result.data))
        self.assertDictEqual(expected_response, res["data"])
        mock_db["booking"].find.assert_called_with(expected_query)

    def test_agent_total_price_weekly_bookings(self):
        request_data = {
            "agent_id": str(users()[1]["_id"]),
            "is_agent": True,
            "filter": "weekly"
        }
        agent_bookings = [bookings()[0], bookings()[1]]
        sat_offset = (date.today().weekday() - 5) % 7
        start_date = date.today() - timedelta(days=sat_offset)
        agent_bookings[0]["booking_date"] = datetime.combine(start_date + timedelta(days=1), time(10, 0, 0))
        agent_bookings[1]["booking_date"] = datetime.combine(start_date + timedelta(days=5), time(0, 0, 0))
        mock_bookings_collection = MagicMock()
        mock_bookings_collection.find.return_value = agent_bookings

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "booking": mock_bookings_collection
        }.get(x)
        expected_query = {
            "$and": [
                {"agent_id": request_data["agent_id"]},
                WeeklySales().get_filter("booking_date")]
        }
        expected_response = WeeklySales().calculate_sales(agent_bookings)
        with self.app.app_context():
            result = fetch_agent_total_price_bookings_timely(request_data, mock_db)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully fetched total price of bookings.", str(result.data))
        self.assertDictEqual(expected_response, res["data"])
        mock_db["booking"].find.assert_called_with(expected_query)

    def test_agent_total_price_monthly_bookings(self):
        request_data = {
            "agent_id": str(users()[1]["_id"]),
            "is_agent": True,
            "filter": "monthly"
        }
        agent_bookings = [bookings()[0], bookings()[1]]
        current_year = datetime.now().year
        agent_bookings[0]["booking_date"] = datetime(current_year, 2, 18)
        agent_bookings[1]["booking_date"] = datetime(current_year, 6, 30)
        mock_bookings_collection = MagicMock()
        mock_bookings_collection.find.return_value = agent_bookings

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "booking": mock_bookings_collection
        }.get(x)
        expected_query = {
            "$and": [
                {"agent_id": request_data["agent_id"]},
                MonthlySales().get_filter("booking_date")]
        }
        expected_response = MonthlySales().calculate_sales(agent_bookings)
        with self.app.app_context():
            result = fetch_agent_total_price_bookings_timely(request_data, mock_db)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully fetched total price of bookings.", str(result.data))
        self.assertDictEqual(expected_response, res["data"])
        mock_db["booking"].find.assert_called_with(expected_query)

    def test_admin_total_price_daily_bookings(self):
        request_data = {
            "is_admin": True,
            "filter": "daily"
        }
        admin_bookings = bookings()
        admin_bookings[0]["booking_date"] = datetime.combine(datetime.now(), time(hour=10, minute=20, second=0))
        admin_bookings[1]["booking_date"] = datetime.combine(datetime.now(), time(hour=15, minute=20, second=0))
        admin_bookings[2]["booking_date"] = datetime.combine(datetime.now(), time(hour=9, minute=20, second=0))
        mock_bookings_collection = MagicMock()
        mock_bookings_collection.find.return_value = admin_bookings

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "booking": mock_bookings_collection
        }.get(x)
        expected_query = DailySales().get_filter("booking_date")
        expected_response = DailySales().calculate_sales(admin_bookings)
        with self.app.app_context():
            result = fetch_total_price_bookings_timely(request_data, mock_db)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully fetched booking sales.", str(result.data))
        self.assertDictEqual(expected_response, res["data"])
        mock_db["booking"].find.assert_called_with(expected_query)

    def test_admin_total_price_weekly_bookings(self):
        request_data = {
            "is_admin": True,
            "filter": "weekly"
        }
        admin_bookings = bookings()
        sat_offset = (date.today().weekday() - 5) % 7
        start_date = date.today() - timedelta(days=sat_offset)
        admin_bookings[0]["booking_date"] = datetime.combine(start_date + timedelta(days=1), time(10, 0, 0))
        admin_bookings[1]["booking_date"] = datetime.combine(start_date + timedelta(days=3), time(10, 0, 0))
        admin_bookings[2]["booking_date"] = datetime.combine(start_date + timedelta(days=5), time(10, 0, 0))
        mock_bookings_collection = MagicMock()
        mock_bookings_collection.find.return_value = admin_bookings

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "booking": mock_bookings_collection
        }.get(x)
        expected_query = WeeklySales().get_filter("booking_date")
        expected_response = WeeklySales().calculate_sales(admin_bookings)

        with self.app.app_context():
            result = fetch_total_price_bookings_timely(request_data, mock_db)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully fetched booking sales.", str(result.data))
        self.assertDictEqual(expected_response, res["data"])
        mock_db["booking"].find.assert_called_with(expected_query)

    def test_admin_total_price_weekly_bookings(self):
        request_data = {
            "is_admin": True,
            "filter": "monthly"
        }
        admin_bookings = bookings()
        current_year = datetime.now().year
        admin_bookings[0]["booking_date"] = datetime(current_year, 2, 18)
        admin_bookings[1]["booking_date"] = datetime(current_year, 7, 19)
        admin_bookings[2]["booking_date"] = datetime(current_year, 10, 20)
        mock_bookings_collection = MagicMock()
        mock_bookings_collection.find.return_value = admin_bookings

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "booking": mock_bookings_collection
        }.get(x)
        expected_query = MonthlySales().get_filter("booking_date")
        expected_response = MonthlySales().calculate_sales(admin_bookings)

        with self.app.app_context():
            result = fetch_total_price_bookings_timely(request_data, mock_db)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully fetched booking sales.", str(result.data))
        self.assertDictEqual(expected_response, res["data"])
        mock_db["booking"].find.assert_called_with(expected_query)

import unittest
from unittest.mock import MagicMock
from flask import current_app
from app.main import app
from schemas.errors import create_error
from enums.roles import Roles
from tests.sample_data.users import users
from tests.sample_data.bookings import bookings

from api_functions.users_api import fetch_agent_details, fetch_agents_list, create_user


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.mock_db = MagicMock()
        with self.app.app_context():
            current_app._get_current_object = lambda: app

    def test_fetch_agents_list(self):
        # Mock the database collection and data
        mock_collection = self.mock_db["user"]
        mock_collection.find.return_value = users()

        with self.app.app_context():
            result = fetch_agents_list({"is_admin": True}, self.mock_db)

        self.assertEqual(len(users()), len(result.get_json()["data"]))
        # Check if the result is as expected
        self.assertEqual(result.status_code, 200)
        self.assertIn("Fetched all agents successfully", str(result.data))

    def test_create_user(self):
        # Mock the database collection and data
        mock_collection = self.mock_db["user"]
        mock_collection.find_one.return_value = None
        request_data = {"email": "test@example.com", "password": "password", "name": "Test User"}

        with self.app.app_context():
            result = create_user({"data": request_data, "role": Roles.ADMIN.value}, self.mock_db)
        # Check if the result is as expected
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully created administrator.", str(result.data))

    def test_create_user_invalid_role(self):
        # Mock the database collection and data
        mock_collection = self.mock_db["user"]
        mock_collection.find_one.return_value = None
        request_data = {"email": "test@example.com", "password": "password", "name": "Test User"}

        with self.app.app_context():
            result = create_user({"data": request_data, "role": "MANAGER"}, self.mock_db)
        payload = result.get_json()
        # Check if the result is as expected
        self.assertEqual(result.status_code, 400)
        self.assertEqual("User role provided is not valid", payload["error"])

    def test_fetch_agent_details(self):

        user_list = users()
        agent_id = str(user_list[1]["_id"])
        agent_name = user_list[1]["name"]

        booking_list = bookings()

        mock_user_collection = MagicMock()
        mock_user_collection.find_one.return_value = user_list[1]
        mock_booking_collection = MagicMock()
        mock_booking_collection.find.return_value = [booking_list[0], booking_list[1]]

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "user": mock_user_collection,
            "booking": mock_booking_collection,
        }.get(x)

        with self.app.app_context():
            result = fetch_agent_details({"agent_id": agent_id}, mock_db)

        result_data = result.get_json("data")
        # Check if the result is as expected
        self.assertEqual(result_data["name"], agent_name)
        self.assertEqual(result_data["total_bookings_sale"], 700.0)
        self.assertEqual(result_data["total_monthly_commission"], 70.0)

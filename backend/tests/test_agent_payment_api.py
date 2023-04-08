import unittest
from unittest import mock
from unittest.mock import MagicMock
from flask import current_app
from datetime import datetime
from flask_pymongo import ObjectId
from enums.payment_status import PaymentStatus
from app.main import app
from tests.sample_data.agent_payments import agent_payments
from tests.sample_data.users import users

from api_functions.agent_payment_api import update_monthly_payment, create_agent_incentive


class TestAgentPayment(unittest.TestCase):
    """
    This module contains unit tests for the AgentPayment functionality.
    The following functions are tested:
    test_update_all_monthly_payments
    test_update_agent_monthly_payments
    test_create_agent_incentive
    test_create_incentive_not_admin
    """

    def setUp(self):
        """
        Set up the unit test for AgentPayment.
        """
        self.app = app
        self.client = self.app.test_client()
        self.mock_db = MagicMock()
        with self.app.app_context():
            current_app._get_current_object = lambda: app

    def test_update_all_monthly_payments(self):
        """
        Test the update_all_monthly_payments function in AgentPayment.
        """
        request_data = {
            "is_admin": True
        }
        mock_payments_collection = MagicMock()
        mock_payments_collection.find.return_value = agent_payments()
        mock_users_collection = MagicMock()
        mock_users_collection.find.return_value = users()

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "agent_payments": mock_payments_collection,
            "users": mock_users_collection
        }.get(x)

        now = datetime.now()
        current_month = now.month
        current_year = now.year
        start_date = datetime(current_year, current_month, 1)
        end_date = datetime(current_year, current_month + 1, 1)
        expected_query = {"$and": [{"status": PaymentStatus.NOT_PAID.value},
                                   {"payment_date": {"$gte": start_date,
                                                     "$lt": end_date}}]}
        with self.app.app_context():
            result = update_monthly_payment(request_data, mock_db)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully updated monthly payments.", str(result.data))
        assert mock_db["agent_payments"].find.call_count == 2
        mock_db["agent_payments"].find.call_args_list[0] == mock.call(expected_query)
        mock_db["agent_payments"].find.call_args_list[0] == mock.call()
        mock_db["users"].find.assert_called_once_with()

    def test_update_agent_monthly_payments(self):
        """
        Test the update_agent_monthly_payments function in AgentPayment.
        """
        request_data = {
            "is_admin": True,
            "agent_id": str(users()[1]["_id"])
        }
        mock_payments_collection = MagicMock()
        mock_payments_collection.find.return_value = agent_payments()
        mock_users_collection = MagicMock()
        mock_users_collection.find.return_value = users()

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "agent_payments": mock_payments_collection,
            "users": mock_users_collection
        }.get(x)

        now = datetime.now()
        current_month = now.month
        current_year = now.year
        start_date = datetime(current_year, current_month, 1)
        end_date = datetime(current_year, current_month + 1, 1)
        expected_query = {"$and": [{"status": PaymentStatus.NOT_PAID.value},
                                   {"payment_date": {"$gte": start_date,
                                                     "$lt": end_date}}, {"agent_id": request_data["agent_id"]}]}
        with self.app.app_context():
            result = update_monthly_payment(request_data, mock_db)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully updated monthly payments.", str(result.data))
        assert mock_db["agent_payments"].find.call_count == 2
        mock_db["agent_payments"].find.call_args_list[0] == mock.call(expected_query)
        mock_db["agent_payments"].find.call_args_list[0] == mock.call()
        mock_db["users"].find.assert_called_once_with({"_id": ObjectId(request_data["agent_id"])})

    def test_create_agent_incentive(self):
        """
        Test the create_agent_incentive function in AgentPayment.
        """
        request_data = {
            "is_admin": True,
            "agent_id": str(users()[1]["_id"]),
            "admin_id": str(users()[3]["_id"]),
            "data": {
                "amount": 104
            }
        }

        mock_payments_collection = MagicMock()
        mock_payments_collection.find.return_value = agent_payments()

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "agent_payment": mock_payments_collection
        }.get(x)

        expected_payload = {
            "amount": 104,
            "pay_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "status": PaymentStatus.NOT_PAID.value,
            "type": "INCENTIVE",
            "agent_id": request_data["agent_id"],
            "created_by": {"admin_id": request_data["admin_id"]}
        }

        with self.app.app_context():
            result = create_agent_incentive(request_data, mock_db)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully added an incentive for the agent.", str(res["data"]))
        mock_db["agent_payment"].insert_one.assert_called_with(expected_payload)

    def test_create_incentive_not_admin(self):
        """
        Test the create_incentive_not_admin function in AgentPayment.
        """
        request_data = {"is_admin": False}
        mock_payments_collection = MagicMock()
        mock_payments_collection.find.return_value = agent_payments()

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "agent_payments": mock_payments_collection,
        }.get(x)
        with self.app.app_context():
            response = create_agent_incentive(request_data, mock_db)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json["error"], "User does not have permission to add an incentive.")
        assert mock_db["agent_payments"].insert_one.call_count <= 0


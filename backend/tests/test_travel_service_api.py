import unittest
from unittest.mock import MagicMock
from flask import current_app
from app.main import app
from enums.service_types import ServiceTypes
from tests.sample_data.travel_services import travel_services
from tests.sample_data.commissions import commissions

from api_functions.travel_service_api import create_travel_service, update_travel_service


class TestTravelService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.mock_db = MagicMock()
        with self.app.app_context():
            current_app._get_current_object = lambda: app

    def test_create_travel_service(self):
        mock_service_collection = MagicMock()
        mock_service_collection.find.return_value = travel_services()
        mock_commission_collection = MagicMock()
        mock_commission_collection.find.return_value = commissions()

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "service": mock_service_collection,
            "commissions": mock_commission_collection,
        }.get(x)
        request_data = {
            "is_admin": True,
            "data": {
                "name": "Emirates",
                "type": ServiceTypes.FLIGHT.value,
                "price": 780,
                "details": {
                    "flight": "E349",
                    "start_loc": "Dubai",
                    "end_loc": "New York"
                }
            }
        }

        with self.app.app_context():
            result = create_travel_service(request_data, mock_db)

        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully created", str(result.data))

    def test_create_travel_service_invalid_type(self):
        mock_service_collection = MagicMock()
        mock_service_collection.find.return_value = travel_services()
        mock_commission_collection = MagicMock()
        mock_commission_collection.find.return_value = commissions()
        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "service": mock_service_collection,
            "commissions": mock_commission_collection,
        }.get(x)
        request_data = {
            "is_admin": True,
            "data": {
                "name": "Emirates",
                "type": "FUN_ACTIVITY",
                "price": 780,
                "details": {
                    "flight": "E349",
                    "start_loc": "Dubai",
                    "end_loc": "New York"
                }
            }
        }

        with self.app.app_context():
            result = create_travel_service(request_data, mock_db)

        self.assertEqual(result.status_code, 400)
        self.assertEqual("Invalid service type provided.", result.get_json()["error"])

    def test_fetch_agent_details(self):

        travel_service_list = travel_services()
        mock_service_collection = MagicMock()
        mock_service_collection.find_one.return_value = travel_service_list[0]
        mock_commission_collection = MagicMock()
        mock_commission_collection.find.return_value = commissions()

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "service": mock_service_collection,
            "commissions": mock_commission_collection,
        }.get(x)

        request_data = {
            "is_admin": True,
            "service_id": str(travel_service_list[0]["_id"]),
            "data": {
                "name": "Emirates",
                "type": ServiceTypes.FLIGHT.value,
                "price": 780,
                "details": {
                    "flight": "E8569",
                    "start_loc": "Dubai",
                    "end_loc": "New York"
                }
            }
        }

        with self.app.app_context():
            result = update_travel_service(request_data, mock_db)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully updated the travel service.", str(result.data))


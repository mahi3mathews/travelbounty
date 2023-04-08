import unittest
from unittest.mock import MagicMock
from flask import current_app, jsonify
from flask_pymongo import ObjectId
from app.main import app
from schemas.itinerary import itinerary_entity, itinerary_list_entity
from schemas.booking import booking_entity, booking_list_entity
from schemas.services import service_list_entity
from tests.sample_data.travel_services import travel_services
from tests.sample_data.bookings import bookings
from tests.sample_data.users import users
from tests.sample_data.itineraries import itineraries

from api_functions.agent_services_api import create_agent_service, fetch_agent_service, fetch_agent_service_list, \
    remove_agent_service


class TestAgentService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.mock_db = MagicMock()
        self.maxDiff = None
        with self.app.app_context():
            current_app._get_current_object = lambda: app

    def test_create_booking_service(self):
        mock_service_collection = MagicMock()
        mock_service_collection.find.return_value = travel_services()
        mock_booking_collection = MagicMock()
        mock_booking_collection.find.return_value = bookings()
        mock_itineraries_collection = MagicMock()
        mock_itineraries_collection.find.return_value = itineraries()
        mock_payments_collection = MagicMock()
        mock_payments_collection.find.return_value = []
        mock_user_collection = MagicMock()
        mock_user_collection.find.return_value = users()
        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "services": mock_service_collection,
            "payments": mock_payments_collection,
            "booking": mock_booking_collection,
            "itineraries": mock_itineraries_collection,
            "users": mock_user_collection
        }.get(x)

        request_data = {
            "data": {
                "service_type": "booking",
                "data": bookings()[0]
            }
        }

        with self.app.app_context():
            result = create_agent_service(request_data, mock_db)

        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully created booking", str(result.data))

    def test_create_itinerary_service(self):
        mock_service_collection = MagicMock()
        mock_service_collection.find.return_value = travel_services()
        mock_booking_collection = MagicMock()
        mock_booking_collection.find.return_value = bookings()
        mock_itineraries_collection = MagicMock()
        mock_itineraries_collection.find.return_value = itineraries()
        mock_payments_collection = MagicMock()
        mock_payments_collection.find.return_value = []
        mock_user_collection = MagicMock()
        mock_user_collection.find.return_value = users()
        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "services": mock_service_collection,
            "payments": mock_payments_collection,
            "booking": mock_booking_collection,
            "itineraries": mock_itineraries_collection,
            "users": mock_user_collection
        }.get(x)

        request_data = {
            "data": {
                "service_type": "itinerary",
                "data": itineraries()[0]
            }
        }

        with self.app.app_context():
            result = create_agent_service(request_data, mock_db)

        self.assertEqual(result.status_code, 200)
        self.assertIn("Successfully created itinerary", str(result.data))

    def test_fetch_itinerary_service(self):
        itinerary_details = itineraries()[0]
        service_list = travel_services()
        itinerary_services = [service_list[0], service_list[2], service_list[4]]

        mock_service_collection = MagicMock()
        mock_service_collection.find.return_value = itinerary_services
        mock_booking_collection = MagicMock()
        mock_booking_collection.find.return_value = bookings()
        mock_itineraries_collection = MagicMock()
        mock_itineraries_collection.find_one.return_value = itinerary_details

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "services": mock_service_collection,
            "bookings": mock_booking_collection,
            "itinerary": mock_itineraries_collection,
        }.get(x)

        request_data = {
            "type": "itinerary",
            "service_id": str(itinerary_details["_id"]),
            "agent_id": ""
        }

        with self.app.app_context():
            result = fetch_agent_service(request_data, mock_db)
            itinerary_res = jsonify(itinerary_entity(itinerary_details, service_list_entity(itinerary_services)))
        self.assertEqual(result.status_code, 200)

        itinerary_data = result.get_json()
        self.assertDictEqual(itinerary_res.get_json(), itinerary_data["data"])
        self.assertEqual("Successfully fetched itinerary details.", itinerary_data["message"])

    def test_fetch_booking_service(self):
        booking_details = bookings()[0]
        service_list = travel_services()
        itinerary_services = [service_list[0], service_list[1], service_list[4]]

        mock_service_collection = MagicMock()
        mock_service_collection.find.return_value = itinerary_services
        mock_booking_collection = MagicMock()
        mock_booking_collection.find_one.return_value = booking_details
        mock_itineraries_collection = MagicMock()
        mock_itineraries_collection.find_one.return_value = itineraries()[0]

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "services": mock_service_collection,
            "bookings": mock_booking_collection,
            "itinerary": mock_itineraries_collection,
        }.get(x)

        request_data = {
            "type": "booking",
            "service_id": str(booking_details["_id"]),
            "agent_id": ""
        }

        with self.app.app_context():
            result = fetch_agent_service(request_data, mock_db)
            booking_res = jsonify(booking_entity(booking_details, service_list_entity(itinerary_services)))
        self.assertEqual(result.status_code, 200)

        booking_data = result.get_json()
        self.assertDictEqual(booking_res.get_json(), booking_data["data"])
        self.assertEqual("Successfully fetched booking details.", booking_data["message"])

    def test_fetch_booking_list(self):
        mock_booking_collection = MagicMock()
        mock_booking_collection.find.return_value = [bookings()[0], bookings()[1]]
        mock_itineraries_collection = MagicMock()
        mock_itineraries_collection.find.return_value = itineraries()

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "bookings": mock_booking_collection,
            "itinerary": mock_itineraries_collection,
        }.get(x)

        request_data = {
            "type": "booking",
            "is_user_exist": True,
            "agent_id": "64201b491451e26ae9b1532a"
        }

        with self.app.app_context():
            result = fetch_agent_service_list(request_data, mock_db)
            bookings_json = jsonify(booking_list_entity([bookings()[0], bookings()[1]]))

        self.assertEqual(result.status_code, 200)

        booking_data = result.get_json()
        expected_bookings = bookings_json.get_json()

        self.assertListEqual(expected_bookings, booking_data["data"])
        self.assertEqual("Successfully fetched all bookings.", booking_data["message"])
        self.assertNotEqual("Successfully fetched all itineraries.", booking_data["message"])

    def test_fetch_itinerary_list(self):
        mock_booking_collection = MagicMock()
        mock_booking_collection.find.return_value = bookings()
        mock_itineraries_collection = MagicMock()
        mock_itineraries_collection.find.return_value = [itineraries()[0], itineraries()[1]]

        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: {
            "bookings": mock_booking_collection,
            "itineraries": mock_itineraries_collection,
        }.get(x)

        request_data = {
            "type": "itinerary",
            "is_user_exist": True,
            "agent_id": "64201b491451e26ae9b1532a"
        }

        with self.app.app_context():
            result = fetch_agent_service_list(request_data, mock_db)
            itineraries_json = jsonify(itinerary_list_entity([itineraries()[0], itineraries()[1]]))

        self.assertEqual(result.status_code, 200)

        itinerary_data = result.get_json()
        expected_itineraries = itineraries_json.get_json()

        self.assertListEqual(expected_itineraries, itinerary_data["data"])
        self.assertEqual("Successfully fetched all itineraries.", itinerary_data["message"])
        self.assertNotEqual("Successfully fetched all bookings.", itinerary_data["message"])

    def test_remove_booking_service(self):
        request_data = {
            "is_agent": True,
            "service_id": bookings()[0]["_id"],
            "service_type": "booking",
            "agent_id": ""
        }
        mock_collections = {
            'itineraries': MagicMock(),
            "bookings": MagicMock(),
            "agent_payments": MagicMock()
        }

        with self.app.app_context():
            result = remove_agent_service(request_data, mock_collections)
        self.assertEqual(result.get_json()["data"], "Successfully removed service.")
        mock_collections['bookings'].delete_one.assert_called_once_with({"_id": ObjectId(request_data['service_id'])})
        mock_collections['itineraries'].assert_not_called()

    def test_remove_itinerary_service(self):
        request_data = {
            "is_agent": True,
            "service_id": itineraries()[0]["_id"],
            "service_type": "itinerary",
            "agent_id": ""

        }
        mock_collections = {
            'itineraries': MagicMock(),
            "bookings": MagicMock(),
            "agent_payments": MagicMock()
        }

        with self.app.app_context():
            result = remove_agent_service(request_data, mock_collections)
        self.assertEqual(result.get_json()["data"], "Successfully removed service.")
        mock_collections['itineraries'].delete_one.assert_called_once_with({"_id": ObjectId(request_data['service_id'])})
        mock_collections['bookings'].assert_not_called()

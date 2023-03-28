from flask_pymongo import ObjectId
from flask import jsonify
from datetime import datetime

from enums.payment_status import PaymentStatus
from schemas.errors import create_error
from schemas.itinerary import create_itinerary_entity, itinerary_entity, itinerary_list_entity
from schemas.booking import create_booking_entity, booking_entity, booking_list_entity
from schemas.payments import create_payment_entity
from schemas.services import service_list_entity
from app.agent import Agent


def create_agent_service(request, db_collections):
    user_collection = db_collections["users"]
    agent_payments_collection = db_collections["payments"]
    itineraries_collection = db_collections["itineraries"]
    bookings_collection = db_collections["booking"]
    services_collection = db_collections["services"]

    payload = request["data"]
    request_data = payload["data"]
    if "service_type" not in payload or "data" not in payload and not payload["data"] or not payload["service_type"]:
        return create_error(400, "Incorrect format of request")
    elif not request_data:
        return create_error(400, "Incorrect/Incomplete booking details.")
    elif "agent_id" not in request_data or not request_data["agent_id"]:
        return create_error(401, "Unauthorized access.")

    agent_user = user_collection.find_one({"_id": ObjectId(request_data["agent_id"])})

    agent = Agent()
    # FACTORY GOF PATTERN
    agent.set_factory_service()
    service_factory = agent.get_factory_service()
    service_obj = service_factory.get_service(payload["service_type"])
    services_list = services_collection.find()
    service_obj.set_services(services_list)
    if services_list is None:
        return create_error(400, "No services found")
    if service_obj.get_type() == "booking":
        if "booking_date" not in request_data or "itinerary_id" not in request_data \
                or "client_info" not in request_data or "payment_type" not \
                in request_data or not request_data["booking_date"] or not \
                request_data["itinerary_id"] or not request_data["client_info"] or \
                not request_data["payment_type"]:
            return create_error(400, "Incorrect/Incomplete request form for booking")
        # Booking created for user by agent
        itinerary = itineraries_collection.find_one({"_id": ObjectId(request_data["itinerary_id"])})

        if itinerary is None:
            return create_error(401, "Provided itinerary does not exist.")
        request_data["services"] = itinerary["services"]
        # MEDIATOR GOF PATTERN
        request_data["total_price"] = service_obj.calculate_total_sales(request_data["services"])
        request_data["total_commission"] = service_obj.calculate_sale_commission(request_data["services"])
        booking_result = bookings_collection.insert_one(create_booking_entity(request_data))
        # Add commission for successful booking
        request_data["amount"] = request_data["total_price"]
        request_data["status"] = PaymentStatus.NOT_PAID.value
        request_data["pay_date"] = datetime.now()
        request_data["type"] = "COMMISSION",
        request_data["created_by"] = {"booking_id": booking_result.inserted_id}
        agent_payments_collection.insert_one(create_payment_entity(request_data))
        user_data = {"booking_count": agent_user["booking_count"] + 1}
    else:
        # Itinerary created by agent
        # MEDIATOR GOF PATTERN
        if "name" not in request_data or "description" not in request_data or "services" not in request_data \
                or not request_data["name"] or not request_data["description"] or not request_data["services"] or \
                len(request_data["services"]) == 0:
            return create_error(400, "Incorrect/Incomplete request form for itinerary")

        request_data["total_commission"] = service_obj.calculate_sale_commission(request_data["services"])
        request_data["total_price"] = service_obj.calculate_total_sales(request_data["services"])
        itineraries_collection.insert_one(create_itinerary_entity(request_data))
        user_data = {"itinerary_count": agent_user["itinerary_count"] + 1}

    user_collection.update_one({"_id": ObjectId(request_data["agent_id"])}, user_data)
    return jsonify({"data": "Successfully created " + service_obj.get_type()})


def fetch_agent_service(request_data, db_collections):
    itineraries_collection = db_collections["itinerary"]
    services_collection = db_collections["services"]
    bookings_collection = db_collections["bookings"]
    service_type = request_data["type"]
    agent = Agent()
    # FACTORY GOF PATTERNS
    agent.set_factory_service()
    factory_obj = agent.get_factory_service()
    service_obj = factory_obj.get_service(service_type)
    if service_obj.get_type() == 'booking':
        booking_details = bookings_collection.find_one({"_id": ObjectId(request_data["service_id"])})
        services_object_ids = []
        for service_id in booking_details["services"]:
            services_object_ids.append(ObjectId(service_id))
        booking_travel_services = service_list_entity(services_collection.find({"_id": {"$in": services_object_ids}}))
        return jsonify({"data": booking_entity(booking_details, booking_travel_services),
                        "message": "Successfully fetched booking details."})
    elif service_obj.get_type() == 'itinerary':
        itinerary_details = itineraries_collection.find_one({"_id": ObjectId(request_data["service_id"])})
        services_object_ids = []
        for service_id in itinerary_details["services"]:
            services_object_ids.append(ObjectId(service_id))
        itinerary_travel_services = service_list_entity(services_collection.find({"_id": {"$in": services_object_ids}}))
        return jsonify({"data": itinerary_entity(itinerary_details, itinerary_travel_services),
                        "message": "Successfully fetched itinerary details."})
    else:
        return create_error(400, "Incorrect request details.")


def fetch_agent_service_list(request_data, db_collections):
    bookings_collection = db_collections["bookings"]
    itineraries_collection = db_collections["itineraries"]
    agent_id = request_data["agent_id"]

    if request_data["is_user_exist"]:
        service_type = request_data["type"]
        agent = Agent()
        # FACTORY GOF PATTERNS
        agent.set_factory_service()
        factory_obj = agent.get_factory_service()
        service_obj = factory_obj.get_service(service_type)
        if service_obj.get_type() == 'booking':
            return jsonify({"data": booking_list_entity(bookings_collection.find({"agent_id": agent_id})),
                            "message": "Successfully fetched all bookings."})
        elif service_obj.get_type() == 'itinerary':
            return jsonify({"data": itinerary_list_entity(itineraries_collection.find({"agent_id": agent_id})),
                            "message": "Successfully fetched all itineraries."})
        else:
            return create_error(400, "Incorrect request details.")
    else:
        return create_error(401, "Unauthorised user access.")


def remove_agent_service(request_data: dict, db_collections):
    if not request_data["is_agent"]:
        return create_error(401, "User does not have permission to remove the booking.")
    elif not request_data['service_id'] or not request_data['service_type']:
        return create_error(400, "Incorrect information provided.")
    else:
        if request_data['service_type'] == "itinerary":
            db_collections['itineraries'].delete_one({"_id": ObjectId(request_data['service_id'])})
        elif request_data["service_type"] == "booking":
            db_collections["bookings"].delete_one({"_id": ObjectId(request_data['service_id'])})
        return jsonify({"data": "Successfully removed service."})

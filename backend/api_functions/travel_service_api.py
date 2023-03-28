from flask import jsonify
from flask_pymongo import ObjectId

from schemas.errors import create_error
from schemas.services import service_entity_create


def calculate_commission(rate, price):
    return (rate/100) * price


def create_travel_service(request_data, db_collections):
    service_data = request_data["data"]
    services_collection = db_collections["service"]
    commission_collection = db_collections["commissions"]

    if not request_data["is_admin"]:
        return create_error(401, "User does not have permission to update services.")
    elif not service_data:
        return create_error(400, "Bad request for creating service!")
    elif "name" not in service_data or "type" not in service_data or "price" not in service_data or \
            "details" not in service_data or not service_data["name"] or \
            not service_data["type"] or not service_data["price"] or \
            not service_data["details"]:
        return create_error(400, "Incomplete/Incorrect service details provided.")
    else:
        commission = commission_collection.find_one({"service": service_data["type"]})
        service_data["commission"] = calculate_commission(commission["commission_rate"], service_data["price"])
        services_collection.insert_one(service_entity_create(service_data))
    return jsonify({"data": "Successfully created"})


def update_travel_service(request_data, db_collections):
    service_data = request_data["data"]
    is_admin = request_data["is_admin"]
    service_id = request_data["service_id"]
    services_collection = db_collections["service"]
    if not is_admin:
        return create_error(401, "User does not have permission to update services.")
    elif not service_data:
        return create_error(400, "Bad request for updating service")
    elif not service_id:
        return create_error(400, "Service id is incorrect.")
    else:
        existing_service = services_collection.find_one({"_id": ObjectId(service_id)})
        if not existing_service:
            return create_error(404, "Service does not exist")
        else:
            services_collection.update_one({"_id": ObjectId(service_id)}, service_data)
            return jsonify({"data": "Successfully updated the travel service."})


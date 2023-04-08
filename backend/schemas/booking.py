from flask import jsonify
from flask_pymongo import ObjectId


def get_booking_status(p_type):
    if not p_type:
        return "NOT PAID"
    else:
        return "PAID"


def create_booking_entity(booking):
    return {
        "booking_date": booking["booking_date"],
        "services": booking["services"],
        "total_price": booking["total_price"],
        "agent_id": str(ObjectId(booking["agent_id"])),
        "status": get_booking_status(booking["payment_type"]),
        "client_info": booking["client_info"],
        "payment_type": booking["payment_type"],
        "itinerary_id": booking["itinerary_id"],
        "total_commission": booking["total_commission"],
        "created_on": booking["created_on"]

    }


def booking_entity(booking, travel_services):
    if not travel_services:
        booking_services = booking["services"]
    else:
        booking_services = travel_services
    booking_res = {
        "id": str(ObjectId(booking["_id"])),
        "booking_date": booking["booking_date"],
        "itinerary_id": str(ObjectId(booking["itinerary_id"])),
        "total_price": booking["total_price"],
        "agent_id": str(ObjectId(booking["agent_id"])),
        "status": booking["status"],
        "client_info": booking["client_info"],
        "payment_type": booking["payment_type"],
        "total_commission": booking["total_commission"],
        "services": booking_services,
        "created_on": booking["created_on"]
    }
    if "itinerary_name" in booking:
        booking_res.update({"itinerary_name": booking["itinerary_name"]})
    if "itinerary_description" in booking:
        booking_res.update({"itinerary_description": booking["itinerary_description"]})

    return booking_res


def booking_list_entity(bookings):
    booking_list = []
    for booking in bookings:
        booking_list.append(booking_entity(booking, None))
    return booking_list

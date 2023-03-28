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
        "payment_type": booking["payment_type"]
    }


def booking_entity(booking, travel_services):
    if not travel_services:
        booking_services = booking["services"]
    else:
        booking_services = travel_services
    return {
        "id": str(ObjectId(booking["_id"])),
        "booking_date": booking["booking_date"],
        "itinerary_id": str(ObjectId(booking["itinerary_id"])),
        "total_price": booking["total_price"],
        "agent_id": str(ObjectId(booking["agent_id"])),
        "status": booking["status"],
        "client_info": booking["client_info"],
        "payment_type": booking["payment_type"],
        "total_commission": booking["total_commission"],
        "services": booking_services
    }


def booking_list_entity(bookings):
    booking_list = []
    for booking in bookings:
        booking_list.append(booking_entity(booking, None))
    return booking_list

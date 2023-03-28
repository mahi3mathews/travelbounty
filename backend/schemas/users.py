from flask import jsonify
from flask_pymongo import ObjectId
from enums.roles import Roles


def user_entity(user):
    response = {
        "user_id": str(ObjectId(user['_id'])),
        "email": user["email"],
        "name": user["name"],
        "role": user["role"],
    }
    if user["role"] != Roles.ADMIN.value:
        if "itinerary_count" not in user or "booking_count" not in user:
            response.update({"itinerary_count": 0, "booking_count": 0})
        else:
            response.update({"itinerary_count": user["itinerary_count"], "booking_count": user["booking_count"]})
    return response


def users_list_entity(users):
    formatted_users = []
    for user in users:
        formatted_users.append(user_entity(user))
    return formatted_users


def agent_details_entity(user):
    response = {
        "user_id": str(ObjectId(user['_id'])),
        "email": user["email"],
        "name": user["name"],
        "role": user["role"],
        "total_bookings_sale": user["total_bookings_sale"],
        "total_monthly_commission": user["total_monthly_commission"]
    }
    if user["role"] != Roles.ADMIN.value:
        if "itinerary_count" not in user or "booking_count" not in user:
            response.update({"itinerary_count": 0, "booking_count": 0})
        else:
            response.update({"itinerary_count": user["itinerary_count"], "booking_count": user["booking_count"]})
    return jsonify(response)

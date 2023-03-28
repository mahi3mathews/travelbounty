from flask import jsonify
from flask_pymongo import ObjectId

from schemas.errors import create_error
from enums.roles import Roles
from schemas.users import users_list_entity, agent_details_entity


def fetch_agents_list(request_data, db_collections):
    user_collection = db_collections["user"]

    if request_data["is_admin"]:

        agents = users_list_entity(user_collection.find({"role": Roles.AGENT.value}))
        return jsonify({"data": agents, "message": "Fetched all agents successfully"})
    else:
        return create_error(401, "User does not have permissions to view all agents")


def create_user(request_details, db_collections):
    request_data = request_details["data"]
    role = request_details["role"]
    user_collection = db_collections["user"]

    if not request_data:
        return create_error(400, "Bad request!")
    elif "email" not in request_data or "password" not in request_data or "name" not in request_data or not \
            request_data["email"] or not request_data["password"] or not request_data["name"]:
        return create_error(400, "Incorrect/Incomplete details provided.")
    else:
        user_collection.insert_one({
            "email": request_data["email"],
            "password": request_data["password"],
            "name": request_data["name"],
            "role": role
        })
        role_value = 'administrator.' if role == Roles.ADMIN.value else "agent."
        return jsonify({"data": "Successfully created " + role_value})


def fetch_agent_details(request_data, db_collections):
    user_collection = db_collections["user"]
    bookings_collection = db_collections["booking"]
    agent_id = request_data["agent_id"]
    agent_details = user_collection.find({"_id": ObjectId(agent_id)})
    total_booking_sale = 0.0
    total_booking_commission = 0.0
    agent_bookings = bookings_collection.find({"agent_id": agent_id})
    for booking in agent_bookings:
        total_booking_sale += booking["total_price"]
        total_booking_commission += booking["total_commission"]
    agent_details["total_bookings_sale"] = total_booking_sale
    agent_details["total_monthly_commission"] = total_booking_commission
    return agent_details_entity(agent_details)

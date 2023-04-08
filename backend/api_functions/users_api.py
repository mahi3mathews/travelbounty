from flask import jsonify
from flask_pymongo import ObjectId

from datetime import datetime, timedelta
from schemas.errors import create_error
from enums.roles import Roles
from schemas.users import users_list_entity, agent_details_entity


def fetch_agents_list(request_data, db_collections):
    """
        This function fetches a list of all agents registered in the system.
        Args:
            request_data (dict): A dictionary containing the request data.
            db_collections (dict): A dictionary containing the database collections.
        Returns:
            A JSON response containing the list of agents and a success message.
    """
    user_collection = db_collections["user"]
    if request_data["is_admin"]:

        agents = users_list_entity(user_collection.find({"role": Roles.AGENT.value}))
        return jsonify({"data": agents, "message": "Fetched all agents successfully"})
    else:
        return create_error(401, "User does not have permissions to view all agents")


def create_user(request_details, db_collections):
    """
    Creates a new user in the system.
    Args:
        request_details: A dictionary containing the user details and role.
        db_collections: A dictionary containing the database collections to be used.
    Returns:
        A JSON response containing a success message if the user was successfully created, or an error message if not.
    """
    request_data = request_details["data"]
    role = request_details["role"]
    user_collection = db_collections["user"]
    admin_user = None
    if role == Roles.ADMIN.value:
        admin_user = user_collection.find_one({"role": Roles.ADMIN.value})
    if not admin_user:
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
    else:
        return create_error(401, "An admin user already exists.")


def fetch_agent_details(request_data, db_collections):
    """
       Helper function to fetch the details of an agent and their booking information.
       Args:
           request_data (dict): A dictionary containing the request data.
               The dictionary has the following format:
               {
                   "agent_id": str
               }
           db_collections (dict): A dictionary containing the database collections.
               The dictionary has the following format:
               {
                   "booking": pymongo.collection.Collection,
                   "user": pymongo.collection.Collection
               }
       Returns:
           dict: A JSON object containing agent details and their booking information.
               The JSON object has the following format:
               {
                   "data": {
                       "id": str,
                       "name": str,
                       "email": str,
                       "role": str,
                       "total_bookings_sale": float,
                       "total_monthly_commission": float,
                       "month_bookings_sale": float
                   },
                   "message": str
               }
               The "id" field is the unique ID of the agent.
               The "name" field is the name of the agent.
               The "email" field is the email address of the agent.
               The "role" field is the role of the agent, which is "AGENT".
               The "total_bookings_sale" field is the total sale amount of all bookings made by the agent.
               The "total_monthly_commission" field is the total commission earned by the agent in the current month.
               The "month_bookings_sale" field is the total sale amount of all bookings made by the agent in the current month.
               The "message" field provides information about the success or failure of the function.
       """
    user_collection = db_collections["user"]
    bookings_collection = db_collections["booking"]
    agent_id = request_data["agent_id"]
    agent_details = user_collection.find_one({"_id": ObjectId(agent_id)})
    total_booking_sale = 0.0
    m_booking_sale = 0.0
    m_booking_commission = 0.0
    total_booking_commission = 0.0
    agent_bookings = bookings_collection.find({"agent_id": agent_id})

    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_end = month_start + timedelta(days=32-month_start.day) - timedelta(seconds=1)
    monthly_query = {"$and": [{"agent_id": agent_id}, {"booking_date": {"$gte": month_start, "$lte": month_end}}]}
    agent_month_bookings = bookings_collection.find(monthly_query)
    for booking in agent_bookings:
        total_booking_sale += booking["total_price"]
        total_booking_commission += booking["total_commission"]
    for m_booking in agent_month_bookings:
        m_booking_sale += m_booking["total_price"]
        m_booking_commission += m_booking["total_commission"]
    booking_info = {"total_bookings_sale": total_booking_sale, "total_monthly_commission": m_booking_commission,
                    "month_bookings_sale": m_booking_sale}
    return agent_details_entity(agent_details, booking_info)

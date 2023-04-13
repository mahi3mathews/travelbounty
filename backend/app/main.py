from flask import Flask, request, jsonify
from flask_pymongo import MongoClient, ObjectId
from flask_cors import CORS
from enums.roles import Roles

from api_functions.agent_services_api import fetch_agent_service_list, fetch_agent_service, create_agent_service, \
    remove_agent_service
from api_functions.travel_service_api import create_travel_service, update_travel_service
from api_functions.users_api import fetch_agents_list, create_user, fetch_agent_details
from api_functions.agent_service_sales_api import fetch_total_price_bookings_timely, \
    fetch_agent_total_price_bookings_timely, fetch_agents_booking_sales, fetch_agent_service_commissions, \
    fetch_service_sales
from api_functions.agent_payment_api import update_monthly_payment, create_agent_incentive, update_single_payment

from schemas.payments import payment_list_entity
from schemas.errors import create_error
from schemas.users import user_entity
from schemas.services import service_entity, service_list_entity
from schemas.commissions_rate import commission_list_entity

app = Flask(__name__)
client = MongoClient("mongodb+srv://mahimathews:a8tHx6I4z7q9pGVf@clustertravelbounty.0droamg.mongodb.net")

CORS(app)

db = client["travelbounty"]
user_collection = db["users"]
bookings_collection = db["bookings"]
agent_payments_collection = db["agent_payments"]
services_collection = db["services"]
itineraries_collection = db["itineraries"]
commission_collection = db["commissions"]


def is_admin(u_id):
    user = user_collection.find_one({"_id": ObjectId(u_id)})
    if not user:
        return False
    elif user.get("role") != Roles.ADMIN.value:
        return False
    else:
        return True


def is_agent(u_id):
    user = user_collection.find_one({"_id": ObjectId(u_id)})
    if not user:
        return False
    elif user.get("role") != Roles.AGENT.value:
        return False
    else:
        return True


def is_user_exist(email, name, u_id):
    if u_id:
        query = {"_id": ObjectId(u_id)}
    else:
        q_email = {"email": email}
        q_name = {"name": name}
        query = {"$and": [q_email, q_name]}
    user = user_collection.find_one(query)
    if user:
        return True
    else:
        return False


@app.route("/api/v1/register-admin", methods=["POST"])
def register_admin():
    """
    This function registers a new agent by creating a new user with the given details in the request payload.
    Returns:
        A response containing a JSON with a success message if the user is successfully registered, otherwise
        an error message
    """
    request_details = {
        "data": request.get_json(),
        "role": Roles.ADMIN.value,
    }
    return create_user(request_details, {"user": user_collection})


@app.route("/api/v1/register-agent", methods=["POST"])
def register_agent():
    """
    Registers a new agent user in the system.
    Returns:
        A JSON response containing a success message if the user was
        successfully registered, or an error message if not.
    """
    request_details = {
        "data": request.get_json(),
        "role": Roles.AGENT.value,
    }
    return create_user(request_details, db_collections={"user": user_collection})


@app.route("/api/v1/login", methods=["POST"])
def login():
    """
    Route to log in a user.
    Returns:
        JSON object: A JSON object containing the user details and a success message if the login
        is successful, or an error message if the login fails.
    """
    request_data = request.get_json()
    email = request_data["email"]
    password = request_data["password"]
    user = user_collection.find_one({"email": email})

    if user:
        if user["password"] == password:
            return jsonify({"data": user_entity(user), "message": 'Successfully logged in.'})
    return create_error(401, "Incorrect credentials. Please try again")


@app.route('/api/v1/users/<user_id>', methods=["GET"])
def get_user_details(user_id):
    """
    Retrieve user details from the database.
    Args:
        user_id: The ID of the user to retrieve.
    Returns:
        A JSON response containing the user details or an error message if the user does not exist.
    """
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return create_error(404, "User does not exist.")
    else:
        return jsonify({"data": user_entity(user), "message": "Successfully fetch user details."})


# TRAVEL SERVICES
@app.route('/api/v1/travel-services', methods=['POST'])
def post_travel_service():
    """
        Create a new travel service.
        Args:
            None
        Returns:
            JSON object containing the newly created travel service and a success message.
        Raises:
            400 Bad Request: If the request data is missing or invalid.
            401 Unauthorized: If the user is not an admin.
            500 Internal Server Error: If there is an error in creating the new travel service.
    """
    request_details = request.get_json()
    admin_id = request_details["userId"]
    request_data = {
        "is_admin": is_admin(admin_id),
        "data": request_details["data"]
    }
    db_collections = {
        "service": services_collection,
        "commissions": commission_collection
    }
    return create_travel_service(request_data, db_collections)


@app.route('/api/v1/travel-services/<service_id>', methods=["PUT"])
def put_travel_service(service_id):
    """
       This function updates the travel service information based on the provided service_id.
       Args:
           service_id (str): The id of the travel service to be updated.
       Returns:
           dict: A JSON response containing the message and data of the updated travel service.
    """
    admin_id = request.get_json()["userId"]
    request_data = {
        "data": request.get_json(),
        "is_admin": is_admin(admin_id),
        "service_id": service_id
    }
    db_collections = {
        "service": services_collection
    }
    return update_travel_service(request_data, db_collections)


@app.route("/api/v1/travel-services", methods=["GET"])
def get_travel_services():
    """
    Retrieve details of a specific travel service.
    Args:
        service_id (str): The ID of the travel service to retrieve.
    Returns:
        dict: A JSON response containing the data and message keys.
            The data key contains the travel service information.
            The message key contains a success message.
    """
    return service_list_entity(services_collection.find())


@app.route("/api/v1/travel-services/<service_id>", methods=["GET"])
def get_travel_service_info(service_id):
    """
       Fetches the details of a travel service based on the given service ID.
       Args:
           service_id (str): The ID of the travel service to fetch.
       Returns:
           A JSON response containing the details of the travel service and a success message.
    """
    return jsonify({"data": service_entity(services_collection.find_one({"_id": ObjectId(service_id)})),
                    "message": "Successfully fetched service details."})


# AGENT USERS
@app.route('/api/v1/<admin_id>/agents', methods=["GET"])
def get_agents_list(admin_id):
    """
       This endpoint fetches a list of all agents registered in the system.
       Args:
           admin_id (str): The ID of the admin user making the request.
       Returns:
           A JSON response containing the list of agents and a success message.
       Raises:
           HTTPException: If the user making the request is not an admin, a 401 error is returned.
       """
    request_data = {
        "is_admin": is_admin(admin_id),
    }
    db_collections = {
        "user": user_collection
    }
    return fetch_agents_list(request_data, db_collections)


@app.route('/api/v1/agents/<agent_id>', methods=["GET"])
def get_agent_details(agent_id):
    """
    Get details of a single agent with given agent ID.
    Args:
        agent_id (str): The ID of the agent.
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
            The "message" field provides information about the success or failure of the API request.
    """
    request_data = {
        "agent_id": agent_id
    }
    db_collections = {
        "booking": bookings_collection,
        "user": user_collection
    }
    return fetch_agent_details(request_data, db_collections)


# COMMISSION RATE
@app.route('/api/v1/<user_id>/commissions', methods=["GET"])
def get_commissions(user_id):
    """
    Retrieves all commission rates from the database.
    Args:
        user_id (str): The user ID to check if the user exists.
    Returns:
        A JSON object containing the commission rates and a success message or an error message
         if the user does not exist.
    """
    if is_user_exist(None, None, user_id):
        return jsonify({"data": commission_list_entity(commission_collection.find()),
                        "message": "Successfully fetched commission rates."})
    else:
        return create_error(404, "User does not exist.")


@app.route('/api/v1/<admin_id>/commissions/<commission_id>', methods=["PUT"])
def update_commission_rate(admin_id, commission_id):
    """
    Update the commission rate for a specific commission in the database.
    Args:
        admin_id (str): The ID of the admin user.
        commission_id (str): The ID of the commission to update.
    Returns:
        A JSON response with the updated list of commissions and a success message.
        If there is an error, returns a JSON error response with an appropriate error message.
    """
    payload = request.get_json()
    if "rate" not in payload or not commission_id or not admin_id:
        return create_error(400, "Incorrect request provided.")
    elif not is_admin(admin_id):
        return create_error(401, "User does not have permission to update the commission rate.")
    else:
        commission_rate = payload["rate"]
        commission_collection.update_one({"_id": ObjectId(commission_id)},
                                         {"$set": {"commission_rate": commission_rate}})
        return jsonify({"data": commission_list_entity(commission_collection.find()),
                        "message": "Successfully updated commission rate."})


# AGENT PAYMENTS
@app.route('/api/v1/<admin_id>/payments', methods=["GET"])
def get_all_payments(admin_id):
    """
       Retrieve all the payments based on status for all agents
       Parameters:
       admin_id (str): The ID of the admin making the request.
       Returns:
       json: A JSON object containing the response data and a message.
    """
    if is_admin(admin_id):
        payment_status = request.args.get("status")
        response = payment_list_entity(agent_payments_collection.find({"status": payment_status}),
                                       list(user_collection.find({"role": Roles.AGENT.value})))
        return jsonify({"data": response,
                        "message": "Successfully fetched all payments."})
    else:
        return create_error(401, "User does not have permission to view payments.")


@app.route('/api/v1/<agent_id>/payments/user', methods=["GET"])
def get_user_payments(agent_id):
    """
    Fetches all payments made to the agent with the specified agent_id and with the given payment status.
    Args:
        agent_id (str): The ID of the agent for whom the payments are being fetched.
    Returns:
        A JSON response containing the payment data and a success message, or an error message if the user
        does not have permission to view payments.
    """
    if is_agent(agent_id):
        payment_status = request.args.get("status")
        query = {"$and": [{"status": payment_status}, {"agent_id": agent_id}]}
        user_query = {"$and": [{"role": Roles.AGENT.value}, ]}
        response = payment_list_entity(agent_payments_collection.find(query),
                                       list(user_collection.find(user_query)))

        return jsonify({"data": response,
                        "message": "Successfully fetched all payments."})
    else:
        return create_error(401, "User does not have permission to view payments.")


@app.route('/api/v1/<admin_id>/payments/pay/<agent_id>', methods=["PUT"])
def put_agent_single_payment(admin_id, agent_id):
    """
    Endpoint to update a single payment status to PAID for a specific agent.
    Args:
        admin_id (str): The ID of the admin user.
        agent_id (str): The ID of the agent whose payment is being updated.
    Returns:
        A JSON response with a success message if the payment status is successfully updated,
        or an error message if the user does not have permission to update payments.
    """
    request_data = {
        "is_admin": is_admin(admin_id),
        "agent_id": agent_id,
        "data": request.get_json()
    }
    db_collections = {
        "agent_payments": agent_payments_collection,
    }
    return update_single_payment(request_data, db_collections)


@app.route('/api/v1/<admin_id>/payments/<agent_id>', methods=["PUT"])
def put_agent_monthly_payment(admin_id, agent_id):
    """
        Update the payment status for a specific agent for the current month.
        Args:
            admin_id (str): The ID of the admin making the request.
            agent_id (str): The ID of the agent whose payment status needs to be updated.
        Returns:
            If successful, returns a JSON object with data containing the updated payment details and message "Successfully updated monthly payment."
            If unsuccessful, returns a JSON object with error details.
    """
    request_data = {
        "is_admin": is_admin(admin_id),
        "agent_id": agent_id
    }
    db_collections = {
        "agent_payments": agent_payments_collection,
        "users": user_collection
    }
    return update_monthly_payment(request_data, db_collections)


@app.route('/api/v1/<admin_id>/payments/all-agents', methods=["PUT"])
def put_agents_monthly_payment(admin_id):
    """
       Update the monthly payments of all agents. If agent_id is given, only updates the payments for that agent.
       Args:
           admin_id (str): ID of the admin making the request.
       Returns:
           JSON: Response containing the updated payment list and success message, or an error message.
    """
    request_data = {
        "is_admin": is_admin(admin_id),
    }
    db_collections = {
        "agent_payments": agent_payments_collection,
        "users": user_collection
    }
    return update_monthly_payment(request_data, db_collections)


@app.route('/api/v1/<admin_id>/payments/<agent_id>/incentive', methods=["POST"])
def post_agent_incentive(admin_id, agent_id):
    """
    Creates a new incentive payment for the specified agent.
    Args:
        admin_id (str): The ID of the admin user making the request.
        agent_id (str): The ID of the agent receiving the incentive.
    Returns:
        A JSON response indicating whether the incentive was successfully added.
    """
    request_data = {
        "data": request.get_json(),
        "admin_id": admin_id,
        "agent_id": agent_id,
        "is_admin": is_admin(admin_id)
    }
    db_collections = {
        "agent_payment": agent_payments_collection
    }
    return create_agent_incentive(request_data, db_collections)


# SALES GRAPH
# all sales based on time
@app.route('/api/v1/service-sales/time', methods=["GET"])
def get_total_price_bookings_timely():
    """
    Route to fetch the total price of bookings made in a specific time
    period (daily, weekly, monthly).
    Returns:
    - JSON object with data and message keys.
    - data: List of dictionaries with booking sales data for each time period.
    - message: Success message.
    Required URL parameters:
    - admin: The ID of the user making the request (admin).
    Optional URL parameters:
    - filter: The time period to filter bookings by (daily, weekly, monthly).
    """
    admin_id = request.args.get("admin")
    request_data = {
        "filter": request.args.get("filter"),
        "is_admin": is_admin(admin_id)
    }
    db_collections = {
        "booking": bookings_collection
    }
    return fetch_total_price_bookings_timely(request_data, db_collections)


# agent sales based on time
@app.route('/api/v1/service-sales/time/agent', methods=["GET"])
def get_agent_total_price_bookings_timely():
    """
       This function returns the total price of bookings for a specific agent based on a time filter.
       Parameters:
       - agent (str): The ID of the agent for whom to fetch the bookings.
       - filter (str): The time filter to apply. Possible values are "daily", "weekly", and "monthly".
       Returns:
       - A JSON object containing the total price of bookings based on the specified filter and agent ID.
       - A success message if the operation was successful.
       - An error message if the user does not have permission to view the bookings or if the filter is invalid.
       """
    agent_id = request.args.get("agent")
    request_data = {
        "filter": request.args.get("filter"),
        "agent_id": agent_id,
        "is_agent": is_agent(agent_id)
    }
    db_collections = {
        "booking": bookings_collection
    }
    return fetch_agent_total_price_bookings_timely(request_data, db_collections)


# all sales based on services and agents
@app.route('/api/v1/service-sales/agents', methods=["GET"])
def get_agents_services_sale():
    """
    Returns the total service sales made by all the agents.
    Args:
        None
    Returns:
        A JSON response containing the total service sales made by all the agents and a success message. If the user
        does not have permission to view all service sales, an error response with a 401 status code is returned.
    """
    admin_id = request.args.get("admin")
    request_data = {
        "is_admin": is_admin(admin_id)
    }
    db_collections = {
        "user": user_collection,
        "booking": bookings_collection,
        "service": services_collection
    }
    return fetch_agents_booking_sales(request_data, db_collections)


# all service sales for admin and agent roles
@app.route('/api/v1/service-sales/user', methods=["GET"])
def get_service_sales():
    """
       Retrieves the total service sales for a user based on their role.
       The user ID is provided as a query parameter.
       Returns:
           A JSON string containing the total service sales and a success message on successful retrieval
           or an error message with a 401 status code if the user does not have permission to view service bookings.
    """
    u_id = request.args.get("user")
    request_data = {
        "u_id": u_id
    }
    db_collections = {
        "user": user_collection,
        "booking": bookings_collection,
        "service": services_collection
    }
    return fetch_service_sales(request_data, db_collections)


# agent commission from all services
@app.route('/api/v1/service-sales/agents-commission', methods=["GET"])
def get_agent_service_commissions():
    """
      Retrieves the total commission earned by an agent for all services booked by them.
      The agent_id is provided as a query parameter.
      Returns:
          A JSON string containing the total service sales and a success message on successful retrieval
          or an error message with a 401 status code if the user does not have permission to view service commissions.
    """
    agent_id = request.args.get("agent")
    request_data = {
        "is_agent": is_agent(agent_id),
        "agent_id": agent_id
    }
    db_collections = {
        "booking": bookings_collection,
        "service": services_collection
    }
    return fetch_agent_service_commissions(request_data, db_collections)


# AGENT SERVICES
@app.route('/api/v1/agent-services', methods=["GET"])
def get_agent_services():
    """
    Get the list of agent services of the given type for the specified agent.
    Args:
        None
    Returns:
        A JSON response containing the list of agent services of the given type for the specified agent,
        or an error message if the request is incorrect or the user is not authorized.
    """
    request_data = {
        "is_user_exist": is_user_exist(None, None, request.args.get('agent')),
        "type": request.args.get("type"),
        "agent_id": request.args.get('agent')
    }
    db_collections = {
        "bookings": bookings_collection,
        "itineraries": itineraries_collection
    }
    return fetch_agent_service_list(request_data, db_collections)


@app.route('/api/v1/agent-services/<service_id>', methods=["GET"])
def get_agent_service_details(service_id):
    """
     Retrieve the details of a booking or itinerary for a given service ID and agent ID.
     Args:
         service_id (str): The service ID to retrieve details for.
     Returns:
         JSON: A JSON object containing the details of the service if it exists.
     Raises:
        HTTPException: If the service type is incorrect, the service does not exist, or the user does not have
        permission to access the service.
     """
    request_data = {
        "type": request.args.get("type"),
        "agent_id": request.args.get("agent"),
        "service_id": service_id
    }
    db_collections = {
        "itinerary": itineraries_collection,
        "services": services_collection,
        "bookings": bookings_collection
    }
    return fetch_agent_service(request_data, db_collections)


@app.route('/api/v1/agent-services/<service_id>', methods=["DELETE"])
def delete_agent_service(service_id):
    """
    Delete the specified agent service.
    Args:
        service_id (str): The ID of the service to be deleted.
    Returns:
        (str): A JSON string representing the result of the operation.
    """
    a_id = request.args.get("agent")
    request_data = {
        "is_agent": is_agent(a_id),
        "service_id": service_id,
        "service_type": request.args.get("type")
    }
    db_collections = {
        "itineraries": itineraries_collection,
        "bookings": bookings_collection,
        "agent_payments": agent_payments_collection
    }
    return remove_agent_service(request_data, db_collections)


@app.route('/api/v1/agent-services', methods=["POST"])
def post_agent_service():
    """
        Create an agent service based on the given request data and database collections.
        Returns:
        A JSON response indicating whether the service was successfully created or not.
        Raises:
        None
    """
    request_data = {
        "data": request.get_json()
    }
    db_collections = {
        "users": user_collection,
        "payments": agent_payments_collection,
        "itineraries": itineraries_collection,
        "booking": bookings_collection,
        "services": services_collection
    }
    return create_agent_service(request=request_data, db_collections=db_collections)


if __name__ == "__main__":
    app.run(debug=True)

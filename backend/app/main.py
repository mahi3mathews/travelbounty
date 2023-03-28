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
from api_functions.agent_payment_api import update_monthly_payment, create_agent_incentive

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
    if not user:
        return True
    else:
        return False


@app.route("/register-admin", methods=["POST"])
def register_admin():
    request_details = {
        "data": request.get_json(),
        "role": Roles.ADMIN.value,
    }
    return create_user(request_details, {"user": user_collection})


@app.route("/register-agent", methods=["POST"])
def register_agent():
    request_details = {
        "data": request.get_json(),
        "role": Roles.AGENT.value,
    }
    return create_user(request_details, db_collections={"user": user_collection})


@app.route("/login", methods=["POST"])
def login():
    email = request.email
    password = request.password
    user = user_collection.find_one({"email": email})
    if user["password"] == password:
        return user_entity(user)
    else:
        return create_error(401, "Incorrect credentials. Please try again")


# ADMIN SERVICES
@app.route('/api/v1/<admin_id>/travel_services', methods=['POST'])
def post_travel_service(admin_id):
    request_data = {
        "is_admin": is_admin(admin_id),
        "data": request.get_json()
    }
    db_collections = {
        "service": services_collection,
        "commissions": commission_collection
    }
    return create_travel_service(request_data, db_collections)


@app.route('/api/v1/<admin_id>/services/<service_id>', methods=["PUT"])
def put_travel_service(admin_id, service_id):
    request_data = {
        "data": request.get_json(),
        "is_admin": is_admin(admin_id),
        "service_id": service_id
    }
    db_collections = {
        "service": services_collection
    }
    return update_travel_service(request_data, db_collections)


@app.route('/api/v1/<admin_id>/agents', methods=["GET"])
def get_agents_list(admin_id):
    request_data = {
        "is_admin": is_admin(admin_id),
    }
    db_collections = {
        "user": user_collection
    }
    return fetch_agents_list(request_data, db_collections)


@app.route('/api/v1/agents/<agent_id>', methods=["GET"])
def get_agent_details(agent_id):
    request_data = {
                       "agent_id": agent_id
                   },
    db_collections = {
        "booking": bookings_collection,
        "user": user_collection
    }
    return fetch_agent_details(request_data, db_collections)


@app.route("/api/v1/services", methods=["GET"])
def get_travel_services():
    return service_list_entity(services_collection.find())


@app.route("/api/v1/services/<service_id>", methods=["GET"])
def get_travel_service_info(service_id):
    return jsonify({"data": service_entity(services_collection.find_one({"_id": ObjectId(service_id)})),
                    "message": "Successfully fetched service details."})


@app.route('/api/v1/<admin_id>/commissions', methods=["GET"])
def get_commissions_for_admin():
    return commission_list_entity(commission_collection.find())


@app.route('/api/v1/<admin_id>/commissions/<commission_id>', methods=["PUT"])
def update_commission_rate(admin_id, commission_id):
    payload = request.get_json()
    if "rate" not in payload or not commission_id or not admin_id:
        return create_error(400, "Incorrect request provided.")
    elif not is_admin(admin_id):
        return create_error(401, "User does not have permission to update the commission rate.")
    else:
        commission_rate = payload["rate"]
        commission_collection.update_one({"_id": ObjectId(commission_id)}, {"commission_rate": commission_rate})
        return commission_list_entity(commission_collection.find())


@app.route('/api/v1/<admin_id>/payments', methods=["GET"])
def get_all_payments(admin_id):
    if is_admin(admin_id):
        payment_status = request.args.get("status")
        return jsonify({"data": payment_list_entity(agent_payments_collection.find({"status": payment_status}),
                                                    user_collection.find({"roles": Roles.AGENT.value})),
                        "message": "Successfully fetched all payments."})
    else:
        return create_error(401, "User does not have permission to view payments.")


@app.route('/api/v1/<admin_id>/payments/<agent_id>', methods=["PUT"])
def put_agent_monthly_payment(admin_id, agent_id):
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


@app.route('/api/v1/<admin_id>/bookings/total_price', methods=["GET"])
def get_total_price_bookings_timely(admin_id):
    request_data = {
        "filter": request.args.get("filter"),
        "is_admin": is_admin(admin_id)
    }
    db_collections = {
        "booking": bookings_collection
    }
    return fetch_total_price_bookings_timely(request_data, db_collections)


@app.route('/api/v1/<agent_id>/bookings', methods=["GET"])
def get_agent_total_price_bookings_timely(agent_id):
    request_data = {
        "filter": request.args.get("filter"),
        "agent_id": agent_id,
        "is_agent": is_agent(agent_id)
    }
    db_collections = {
        "booking": bookings_collection
    }
    return fetch_agent_total_price_bookings_timely(request_data, db_collections)


@app.route('/api/v1/<admin_id>/agents/service-sales', methods=["GET"])
def get_agents_services_sale(admin_id):
    request_data = {
        "is_admin": is_admin(admin_id)
    }
    db_collections = {
        "user": user_collection,
        "booking": bookings_collection,
        "service": services_collection
    }
    return fetch_agents_booking_sales(request_data, db_collections)


@app.route('/api/v1/<agent_id>/service-bookings/agents-commission', methods=["GET"])
def get_agent_service_commissions(agent_id):
    request_data = {
        "is_agent": is_agent(agent_id),
        "agent_id": agent_id
    }
    db_collections = {
        "booking": bookings_collection,
        "service": services_collection
    }
    return fetch_agent_service_commissions(request_data, db_collections)


@app.route('/api/v1/<u_id>/service-sales', methods=["GET"])
def get_service_sales(u_id):
    request_data = {
        "u_id": u_id
    }
    db_collections = {
        "user": user_collection,
        "booking": bookings_collection,
        "service": services_collection
    }
    return fetch_service_sales(request_data, db_collections)


@app.route('/api/v1/<agent_id>/agent-services', methods=["GET"])
def get_agent_services(agent_id):
    request_data = {
        "is_user_exist": is_user_exist(None, None, agent_id),
        "type": request.args.get("type"),
        "agent_id": agent_id
    }
    db_collections = {
        "bookings": bookings_collection,
        "itineraries": itineraries_collection
    }
    return fetch_agent_service_list(request_data, db_collections)


@app.route('/api/v1/agent-services/<service_id>', methods=["GET"])
def get_agent_service_details(service_id):
    request_data = {
        "type": request.args.get("type"),
        "service_id": service_id
    }
    db_collections = {
        "itinerary": itineraries_collection,
        "services": services_collection,
        "bookings": bookings_collection
    }
    return fetch_agent_service(request_data, db_collections)


@app.route('/api/v1/<a_id>/agent-services/<service_type>/<service_id>', methods=["DELETE"])
def delete_agent_service(a_id, service_type, service_id):
    request_data = {
        "is_agent": is_agent(a_id),
        "service_id": service_id,
        "service_type": service_type
    }
    db_collections = {
        "itineraries": itineraries_collection,
        "bookings": bookings_collection
    }
    return remove_agent_service(request_data, db_collections)


@app.route('/api/v1/agent-services', methods=["POST"])
def post_agent_service():
    request_data = {
        "data": request.get_json()
    }
    db_collections = {
        "users": user_collection,
        "payments": agent_payments_collection,
        "itineraries": itineraries_collection,
        "bookings": bookings_collection,
        "services": services_collection
    }
    return create_agent_service(request=request_data, db_collections=db_collections)


if __name__ == "__main__":
    app.run(debug=True)

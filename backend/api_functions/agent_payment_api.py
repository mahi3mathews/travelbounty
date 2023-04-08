from datetime import datetime
from flask import jsonify
from flask_pymongo import ObjectId

from enums.payment_status import PaymentStatus
from schemas.payments import payment_list_entity, create_payment_entity
from schemas.errors import create_error


def update_single_payment(request_data, db_collections):
    """
    Function to update a single payment status to PAID for a specific agent.
    Args:
        request_data (dict): A dictionary containing request data.
        db_collections (dict): A dictionary containing database collections.
    Returns:
        A JSON response with a success message if the payment status is successfully updated,
        or an error message if the user does not have permission to update payments.
    """
    agent_payments_collection = db_collections["agent_payments"]
    data = request_data["data"]
    payment_id = data["payment_id"]
    if request_data["is_admin"]:
        agent_payments_collection.update_one({"_id": ObjectId(payment_id)},
                                             {"$set": {"status": PaymentStatus.PAID.value}})
        return jsonify({"data": "Successfully updated single payment."})
    else:
        return create_error(401, "User does not have permission to update payments.")


def update_monthly_payment(request_data, db_collections):
    """
     Update the monthly payments of all agents. If agent_id is given, only updates the payments for that agent.
     Args:
         request_data (dict): Dictionary containing request data.
         db_collections (dict): Dictionary containing database collections.
     Returns:
         JSON: Response containing the updated payment list and success message, or an error message.
     """
    agent_payments_collection = db_collections["agent_payments"]
    user_collection = db_collections["users"]
    if request_data["is_admin"]:
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        start_date = datetime(current_year, current_month, 1)
        end_date = datetime(current_year, current_month + 1, 1)

        unpaid_queries = [{"status": PaymentStatus.NOT_PAID.value}, {"payment_date": {"$gte": start_date,
                                                                                      "$lt": end_date}}]

        if "agent_id" in request_data and request_data["agent_id"]:
            agent_id = request_data["agent_id"]
            unpaid_queries.append({"agent_id": agent_id})
            user_data = user_collection.find({"_id": ObjectId(agent_id)})
        else:
            user_data = user_collection.find()
        overall_query = {"$and": unpaid_queries}
        unpaid_payments = agent_payments_collection.find(overall_query)

        for payment in unpaid_payments:
            agent_payments_collection.update_one({"_id": payment["_id"]}, {"$set":{"status": PaymentStatus.PAID.value}})
        return jsonify({"data": payment_list_entity(agent_payments_collection.find(), user_data),
                        "message": "Successfully updated monthly payments."})
    else:
        return create_error(401, "User does not have permission to update payments.")


def create_agent_incentive(request_data, db_collections):
    """
       Creates a new payment entity for an agent incentive and adds it to the agent payments collection in the database.
       Args:
           request_data (dict): A dictionary containing the request data, including the admin ID, agent ID, and payment payload.
           db_collections (dict): A dictionary containing the database collections.
       Returns:
           A JSON response indicating whether the incentive was successfully added.
    """
    if request_data["is_admin"]:
        admin_id = request_data["admin_id"]
        agent_id = request_data["agent_id"]
        payload = request_data["data"]
        agent_payments_collection = db_collections["agent_payment"]
        payload["pay_date"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        payload["status"] = PaymentStatus.NOT_PAID.value
        payload["type"] = "INCENTIVE"
        payload["agent_id"] = agent_id
        payload["created_by"] = {"admin_id": admin_id}
        agent_payments_collection.insert_one(create_payment_entity(payload))
        return jsonify({"data": "Successfully added an incentive for the agent."})
    else:
        return create_error(401, "User does not have permission to add an incentive.")

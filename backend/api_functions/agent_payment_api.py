from datetime import datetime
from flask import jsonify
from flask_pymongo import ObjectId

from enums.payment_status import PaymentStatus
from schemas.payments import payment_list_entity, create_payment_entity
from schemas.errors import create_error


def update_monthly_payment(request_data, db_collections):
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
            user_query = {"_id": ObjectId(agent_id)}
            unpaid_queries.append({"agent_id": agent_id})
            user_data = user_collection.find({"_id": ObjectId(agent_id)})
        else:
            user_data = user_collection.find()
        overall_query = {"$and": unpaid_queries}
        unpaid_payments = agent_payments_collection.find(overall_query)

        for payment in unpaid_payments:
            agent_payments_collection.update_one({"_id": payment["_id"]}, {"status": PaymentStatus.PAID.value})
        return jsonify({"data": payment_list_entity(agent_payments_collection.find(), user_data),
                        "message": "Successfully updated monthly payments."})
    else:
        return create_error(401, "User does not have permission to update payments.")


def create_agent_incentive(request_data, db_collections):
    if request_data["is_admin"]:
        admin_id = request_data["admin_id"]
        agent_id = request_data["agent_id"]
        payload = request_data["data"]
        agent_payments_collection = db_collections["agent_payment"]
        payload["pay_date"] = datetime.now()
        payload["status"] = PaymentStatus.NOT_PAID.value
        payload["type"] = "INCENTIVE"
        payload["agent_id"] = agent_id
        payload["created_by"] = {"admin_id": admin_id}
        agent_payments_collection.insert_one(create_payment_entity(payload))
        return jsonify({"data": "Successfully added an incentive for the agent."})
    else:
        return create_error(401, "User does not have permission to add an incentive.")

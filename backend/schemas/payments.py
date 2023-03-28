from flask import jsonify
from flask_pymongo import ObjectId


def create_payment_entity(payment):
    return {
        "agent_id": str(ObjectId(payment["agent_id"])),
        "amount": payment["amount"],
        "pay_date": payment["pay_date"],
        "status": payment["status"],
        "type": payment["type"],
        "created_by": payment["created_by"]
    }


def payment_entity(payment, agent):
    return {
        "id": str(ObjectId(payment["_id"])),
        "agent_id": str(ObjectId(agent["_id"])),
        "agent_name": agent["name"],
        "amount": payment["amount"],
        "pay_date": payment["pay_date"],
        "status": payment["status"],
        "type": payment["type"]
    }


def payment_list_entity(payments, agents):
    payment_list = []
    for payment in payments:
        agent = [x for x in agents if str(ObjectId(x["_id"])) == payment["agent_id"]]
        payment_list.append(payment_entity(payment, agent[0]))
    return payment_list

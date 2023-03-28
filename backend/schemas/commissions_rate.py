from flask import jsonify
from flask_pymongo import ObjectId


def commission_entity(commission):
    return jsonify({
        "id": str(ObjectId(commission["_id"])),
        "commission_rate": commission["commission_rate"],
        "service_type": commission["service"]
    })


def commission_list_entity(commissions):
    commission_list = []
    for commission in commissions:
        commission_list.append(commission_entity(commission))
    return commission_list


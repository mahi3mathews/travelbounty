from flask import jsonify
from flask_pymongo import ObjectId


def service_entity_create(services):
    return {
        "name": services["name"],
        "price": services["price"],
        "type": services["type"],
        "details": services["details"],
        "commission": services["commission"]
    }


def service_entity(services: dict):
    return {
        "name": services["name"],
        "price": services["price"],
        "type": services["type"],
        "details": services["details"],
        "id": str(ObjectId(services["_id"]))
    }


def service_list_entity(service_list: list):
    s_list = []
    for service in service_list:
        s_list.append(service_entity(service))
    return s_list

from flask import jsonify
from flask_pymongo import ObjectId


def create_itinerary_entity(itinerary):
    return {
        "agent_id": itinerary["agent_id"],
        "services": itinerary["services"],
        "total_price": itinerary["total_price"],
        "name": itinerary["name"],
        "description": itinerary["description"],
        "total_commission": itinerary["total_commission"]
    }


def itinerary_entity(itinerary, travel_services):
    if not travel_services:
        itinerary_services = itinerary["services"]
    else:
        itinerary_services = travel_services
    return {
        "id": str(ObjectId(itinerary["_id"])),
        "agent_id": itinerary["agent_id"],
        "services": itinerary_services,
        "total_price": itinerary["total_price"],
        "name": itinerary["name"],
        "description": itinerary["description"],
        "total_commission": itinerary["total_commission"]
    }


def itinerary_list_entity(itinerary_list):
    i_list = []
    for itinerary in itinerary_list:
        i_list.append(itinerary_entity(itinerary, None))
    return i_list

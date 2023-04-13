from datetime import datetime
from flask_pymongo import ObjectId


def bookings():
    return [{
        "_id": ObjectId("64185fa6243ffef77ce1cc0f"),
        "agent_id": "64201b491451e26ae9b1532a",
        "itinerary_id": "641ec2aa895625004ec93007",
        "services": ["641eb2a788d9a053e4054a4e", "641eb29c9b2f3a0cbaa4ee34",
                     "641eb2953d0171e92a395dc2"],
        "booking_date": datetime.now(),
        "total_commission": 20,
        "total_price": 100,
        "status": "PAID",
        "created_on": datetime.now(),
        "payment_type": "CARD",
        "client_info": {
            "name": "Sam",
            "phone_number": "0183848993",
            "email": "sam@gmail.com",
            "age": 22
        }},
        {
            "_id": ObjectId("64185f31243ffef77ce1cc0d"),
            "agent_id": "64201b491451e26ae9b1532a",
            "itinerary_id": "641ec2b1e65a7fdc07ab66c9",
            "services": ["641eb28b48472e33df53441c", "641eb2953d0171e92a395dc2",
                         "641eb29c9b2f3a0cbaa4ee34"],
            "booking_date": datetime.now(),
            "total_commission": 50,
            "total_price": 600,
            "status": "PAID",
            "created_on": datetime.now(),
            "payment_type": "CARD",
            "client_info": {
                "name": "Robin T",
                "phone_number": "01838432493",
                "email": "robin@gmail.com",
                "age": 29
            }
        },
        {
            "_id": ObjectId("64185f7f243ffef77ce1cc0e"),
            "agent_id": "64201b511d22bcefdfd70141",
            "itinerary_id": "641ec2b7c2024af2ec21532e",
            "services": ["641eb29c9b2f3a0cbaa4ee34", "641eb2a788d9a053e4054a4e", "641eb28b48472e33df53441c"],
            "booking_date": datetime.now(),
            "total_commission": 26,
            "total_price": 200,
            "status": "PAID",
            "payment_type": "CARD",
            "created_on": datetime.now(),
            "client_info": {
                "name": "Mariya T",
                "phone_number": "01838432493",
                "email": "mariya@gmail.com",
                "age": 23
            }}
    ]

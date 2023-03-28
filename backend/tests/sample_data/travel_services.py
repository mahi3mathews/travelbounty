from datetime import datetime
from flask_pymongo import ObjectId


def travel_services():
    return [
        {
            "_id": ObjectId("641eb2a788d9a053e4054a4e"),
            "name": "AirAsia",
            "type": "FLIGHT",
            "price": 200,
            "commission": 20,
            "details": {
                "start_loc": "Toronto",
                "end_loc": "Malaysia",
                "start_time": datetime(2023, 7, 4),
                "service_level": "BUSINESS",
                "flight": "AS183"
            }
        },
        {
            "_id": ObjectId("641eb29c9b2f3a0cbaa4ee34"),
            "name": "Marriott Hotel",
            "type": "ACCOMMODATION",
            "price": 1200,
            "commission": 240,
            "details": {
                "loc": "London",
                "suite": '10',
            }
        },
        {
            "_id": ObjectId("641ec4c31b69ecb326f996b0"),
            "name": "ABC Resort",
            "type": "ACCOMMODATION",
            "price": 900,
            "commission": 180,
            "details": {
                "loc": "Malaysia",
                "suite": 'deluxe-10',
            }
        },
        {
            "_id": ObjectId("641ec4c965f5e3003f6d53a0"),
            "name": "Snorkeling",
            "type": "ACTIVITY",
            "price": 300,
            "commission": 15,
            "details": {
                "loc": "Malaysia",
                "time": datetime(2023, 11, 20)
            }
        },
        {
            "_id": ObjectId("641eb2953d0171e92a395dc2"),
            "name": "Ariana Concert",
            "type": "ACTIVITY",
            "price": 130,
            "commission": 6.5,
            "details": {
                "loc": "London",
                "time": datetime(2023, 11, 20)
            }
        },
        {
            "_id": ObjectId("641eb28b48472e33df53441c"),
            "name": "London City trip",
            "type": "TRANSPORTATION",
            "price": 140,
            "commission": 19.5,
            "details": {
                "start_loc": "13 Baker Street",
                "start_time": datetime(2023, 10, 20),
                "end_loc": "Thames River"

            }
        }
    ]

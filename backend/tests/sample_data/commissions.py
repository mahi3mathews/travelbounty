from flask_pymongo import ObjectId


def commissions():
    return [
        {
            "_id": ObjectId("64185f31243ffef77ce1cc0d"),
            "commission_rate": 10,
            "service": "FLIGHT"
        },
        {
            "_id": ObjectId("64185f7f243ffef77ce1cc0e"),
            "commission_rate": 20,
            "service": "ACCOMMODATION"
        }, {
            "_id": ObjectId("64185fa6243ffef77ce1cc0f"),
            "commission_rate": 11,
            "service": "ACTIVITY"
        }, {
            "_id": ObjectId("64185fc4243ffef77ce1cc10"),
            "commission_rate": 15,
            "service": "TRANSPORTATION"
        }
    ]

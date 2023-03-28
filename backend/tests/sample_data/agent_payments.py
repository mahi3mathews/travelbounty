from datetime import datetime
from flask_pymongo import ObjectId
from enums.payment_status import PaymentStatus


def agent_payments():
    return [
        {
            "agent_id": "64201b491451e26ae9b1532a",
            "_id": ObjectId("6422aaf0989151af2bc657fb"),
            "pay_date": datetime(2023, 3, 31),
            "status": PaymentStatus.NOT_PAID.value,
            "type": "INCENTIVE",
            "amount": 80,
            "created_by": {"admin_id": "64201b58b90be1a7965e4e4a"}
        },
        {
            "agent_id": "64201b491451e26ae9b1532a",
            "_id": ObjectId("6422ac2932f330e04735d349"),
            "pay_date": datetime(2023, 3, 31),
            "status": PaymentStatus.NOT_PAID.value,
            "type": "BOOKING",
            "amount": 90,
            "created_by": {"booking_id": "64185fa6243ffef77ce1cc0f"}
        },
        {
            "agent_id": "64201b491451e26ae9b1532a",
            "_id": ObjectId("6422ac311481872966947c1e"),
            "pay_date": datetime(2023, 3, 31),
            "status": PaymentStatus.NOT_PAID.value,
            "type": "BOOKING",
            "amount": 80,
            "created_by": {"booking_id": "64185f31243ffef77ce1cc0d"}
        },
        {
            "agent_id": "64201b511d22bcefdfd70141",
            "_id": ObjectId("6422ac37aed2ea12b7673b44"),
            "pay_date": datetime(2023, 3, 31),
            "status": PaymentStatus.NOT_PAID.value,
            "type": "BOOKING",
            "amount": 80,
            "created_by": {"booking_id": "64185f7f243ffef77ce1cc0e"}
        }
    ]

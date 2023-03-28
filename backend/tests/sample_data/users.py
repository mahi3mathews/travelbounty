from flask_pymongo import ObjectId
from enums.roles import Roles


def users():
    return [
        {
            "name": "Same T",
            "email": "sam@ams.com",
            "_id": ObjectId("64201b3151d53299e6528e13"),
            "password": "password1",
            "role": Roles.AGENT.value,
        },
        {
            "name": "Seline Cooper",
            "email": "seline@ams.com",
            "_id": ObjectId("64201b491451e26ae9b1532a"),
            "password": "password1",
            "role": Roles.AGENT.value,
        },
        {
            "name": "Talia K",
            "email": "talia@ams.com",
            "_id": ObjectId("64201b511d22bcefdfd70141"),
            "password": "password1",
            "role": Roles.AGENT.value,
        },
        {
            "name": "Leyla C",
            "email": "leyla@ams.com",
            "_id": ObjectId("64201b58b90be1a7965e4e4a"),
            "password": "password1",
            "role": Roles.ADMIN.value,
        }
    ]

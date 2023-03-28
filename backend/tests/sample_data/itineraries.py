from flask_pymongo import ObjectId


def itineraries():
    return [
        {
            "_id": ObjectId("641ec2aa895625004ec93007"),
            "agent_id": "64201b491451e26ae9b1532a",
            "services": ["641eb2a788d9a053e4054a4e", "641ec4c31b69ecb326f996b0", "641ec4c965f5e3003f6d53a0"],
            "total_commission": 20,
            "total_price": 100,
            "name": "Malaysian beach packages",
            "description": "A business class flight from Toronto to Malaysia after which a stay in a luxurious resort"
                           " with sea-facing deluxe room with a tour showing the beauty of the ocean." 
                           "A snorkeling activity is available to take the client to new levels of sea to experience "
                           "different parts of the ocean."

        },
        {
            "_id": ObjectId("641ec2b1e65a7fdc07ab66c9"),
            "agent_id": "64201b491451e26ae9b1532a",
            "services": ["641eb28b48472e33df53441c", "641eb2953d0171e92a395dc2", "641eb29c9b2f3a0cbaa4ee34"],
            "total_commission": 50,
            "total_price": 600,
            "name": "London rural city package",
            "description": "A stay in a luxurious 5-star hotel with a tour showing the beauty of London city starting"
                           " from world famous Baker street to the Thames river. With the end of viewing London "
                           "city, a flight back to Malaysia via Toronto completes the package."

        },
        {
            "_id": ObjectId("641ec2b7c2024af2ec21532e"),
            "agent_id": "64201b511d22bcefdfd70141",
            "services": ["641eb29c9b2f3a0cbaa4ee34", "641eb2a788d9a053e4054a4e", "641eb28b48472e33df53441c"],
            "total_commission": 26,
            "total_price": 200,
            "name": "London rural city package",
            "description": "A stay in a luxurious 5-star hotel with a tour showing the beauty of London city starting"
                           " from world famous Baker street to the Thames river. With the end of viewing London "
                           "city, a flight back to Malaysia via Toronto completes the package."
        }

    ]

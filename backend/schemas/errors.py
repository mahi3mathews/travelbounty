from flask import jsonify, make_response


def create_error(status, message):
    return make_response(jsonify({"error": message, "status": status}), status)


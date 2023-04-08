from flask import jsonify, make_response


def create_error(status, message):
    """
    Creates a JSON response with the given status code and error message.
    Args:
        status (int): The HTTP status code to include in the response.
        message (str): The error message to include in the response.
    Returns:
        A JSON response containing the error message and status code.
    """
    return make_response(jsonify({"error": message, "status": status}), status)


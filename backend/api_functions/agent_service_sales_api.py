from flask import jsonify
from flask_pymongo import ObjectId

from enums.roles import Roles
from schemas.errors import create_error
from schemas.booking import booking_list_entity
from app.booking_sales_by_time import BookingSalesByTime
from app.admin import Admin
from app.agent import Agent


def fetch_total_price_bookings_timely(request_data, db_collections):
    """
    Function to fetch the total price of bookings made in a specific time period (daily, weekly, monthly).
    Args:
    - request_data: Dictionary containing request data, including filter and admin ID.
    - db_collections: Dictionary containing database collections.
    Returns:
    - JSON object with data and message keys.
    - data: List of dictionaries with booking sales data for each time period.
    - message: Success message.
    """
    bookings_collection = db_collections["booking"]
    query_filter = request_data["filter"]
    if not request_data["is_admin"]:
        return create_error(401, "User does not have permission to view all booking sales.")
    elif not query_filter:
        return create_error(400, "Filter is not provided.")
    else:
        # FACADE GOF PATTERN
        booking_sales = BookingSalesByTime()
        if query_filter == "daily":
            d_bookings = bookings_collection.find(booking_sales.get_daily_filter("created_on"))
            response = booking_sales.get_daily_sales(list(d_bookings))
        elif query_filter == "monthly":
            m_bookings = bookings_collection.find(booking_sales.get_monthly_filter("created_on"))
            response = booking_sales.get_monthly_sales(list(m_bookings))
        elif query_filter == "weekly":
            w_bookings = bookings_collection.find(booking_sales.get_weekly_filter("created_on"))
            response = booking_sales.get_weekly_sales(list(w_bookings))

    return jsonify({"data": response, "message": "Successfully fetched booking sales."})


def fetch_agent_total_price_bookings_timely(request_data, db_collections):
    """
        This function fetches the bookings for a specific agent based on a time filter, calculates the total price of the bookings,
        and returns the result.
        Parameters:
        - request_data (dict): A dictionary containing the filter, agent ID, and agent permission information.
        - db_collections (dict): A dictionary containing the MongoDB collections to use.
        Returns:
        - A JSON object containing the total price of bookings based on the specified filter and agent ID.
        - A success message if the operation was successful.
        - An error message if the user does not have permission to view the bookings or if the filter is invalid.
    """
    bookings_collection = db_collections["booking"]
    agent_id = request_data["agent_id"]

    query_filter = request_data["filter"]
    if not request_data["is_agent"]:
        return create_error(401, "User does not have permission to view this booking filter.")
    elif not query_filter:
        return jsonify({"data": booking_list_entity(bookings_collection.find({"agent_id": agent_id})),
                        "message": "Successfully fetched all bookings."})
    else:
        # FACADE GOF PATTERN
        booking_sales = BookingSalesByTime()
        agent_query = {"agent_id": agent_id}
        if query_filter == "daily":
            booking_query = booking_sales.get_daily_filter("created_on")
            query = {"$and": [agent_query, booking_query]}
            d_bookings = bookings_collection.find(query)
            response = booking_sales.get_daily_sales(d_bookings)
        elif query_filter == "monthly":
            booking_query_month = booking_sales.get_monthly_filter("created_on")
            query_month = {"$and": [agent_query, booking_query_month]}
            m_bookings = bookings_collection.find(query_month)
            response = booking_sales.get_monthly_sales(m_bookings)
        elif query_filter == "weekly":
            booking_query_week = booking_sales.get_weekly_filter("created_on")
            query_year = {"$and": [agent_query, booking_query_week]}
            w_bookings = bookings_collection.find(query_year)
            response = booking_sales.get_weekly_sales(w_bookings)

    return jsonify({"data": response, "message": "Successfully fetched total price of bookings."})


def fetch_agents_booking_sales(request_data, db_collections):
    """
    Calculates and returns the total service sales made by all the agents.
    Args:
        request_data (dict): A dictionary containing the request data.
        db_collections (dict): A dictionary containing the database collections.
    Returns:
        A JSON response containing the total service sales made by all the agents and a success message. If the user
        does not have permission to view all service sales, an error response with a 401 status code is returned.
    """
    bookings_collection = db_collections["booking"]
    services_collection = db_collections["service"]
    user_collection = db_collections["user"]
    if not request_data["is_admin"]:
        return create_error(401, "User does not have permission to view all service sales.")
    else:
        admin = Admin()
        # FACTORY GOF PATTERN
        admin.set_factory_service()
        booking_obj = admin.get_factory_service().get_service("booking")
        # MEDIATOR GOF PATTERN
        booking_obj.set_services(list(services_collection.find()))
        booking_obj.set_bookings(list(bookings_collection.find()))
        output = booking_obj.calculate_sale_by_agent(list(user_collection.find({"role": Roles.AGENT.value})))
        return jsonify({"data": output, "message": "Successfully fetched the services booked by agents."})


def fetch_agent_service_commissions(request_data, db_collections):
    """
      Fetches the total commission earned by an agent for all services booked by them.
      Args:
          request_data: A dictionary containing information about the agent.
              is_agent: A boolean indicating whether the agent exists or not.
              agent_id: An integer representing the agent ID.
          db_collections: A dictionary containing database collections.
              booking: A collection representing bookings made by agents.
              service: A collection representing services provided by the company.
      Returns:
          A JSON string containing the total service sales and a success message on successful retrieval.
    """
    if request_data["is_agent"]:
        bookings_collection = db_collections["booking"]
        services_collection = db_collections["service"]
        agent_id = request_data["agent_id"]
        user_obj = Agent()
        # FACTORY GOF PATTERN
        user_obj.set_factory_service()
        service_obj = user_obj.get_factory_service()
        booking_obj = service_obj.get_service("booking")
        booking_obj.set_services(list(services_collection.find()))
        booking_obj.set_bookings(list(bookings_collection.find({"agent_id": agent_id})))
        # MEDIATOR GOF PATTERN
        total_service_sales = booking_obj.calculate_all_services_commission()
        return jsonify({"data": total_service_sales, "message": "Successfully fetched all services commissions."})
    else:
        return create_error(401, "User does not have permission to view service commissions")


def fetch_service_sales(request_data, db_collections):
    """
        Fetches the total service sales for a user based on their role.
        Args:
            request_data: A dictionary containing information about the user.
                u_id: A string representing the user ID.
            db_collections: A dictionary containing database collections.
                user: A collection representing user data.
                booking: A collection representing bookings made by agents.
                service: A collection representing services provided by the company.
        Returns:
            A JSON string containing the total service sales and a success message on successful retrieval
            or an error message with a 401 status code if the user does not have permission to view service bookings.
    """
    bookings_collection = db_collections["booking"]
    services_collection = db_collections["service"]
    user_collection = db_collections["user"]
    u_id = request_data["u_id"]
    user = user_collection.find_one({"_id": ObjectId(u_id)})
    if user:
        if user["role"] == Roles.ADMIN.value:
            user_obj = Admin()
            bookings_list = bookings_collection.find()
        else:
            user_obj = Agent()
            bookings_list = bookings_collection.find({"agent_id": u_id})
        # FACTORY GOF PATTERN
        user_obj.set_factory_service()
        service_obj = user_obj.get_factory_service()
        booking_obj = service_obj.get_service("booking")
        booking_obj.set_services(list(services_collection.find()))
        booking_obj.set_bookings(bookings_list)
        # MEDIATOR GOF PATTERN
        total_service_sales = booking_obj.calculate_all_services_sale()

        return jsonify({"data": total_service_sales, "message": "Successfully fetched all services sales."})
    else:
        return create_error(401, "User does not have permission to view service bookings")

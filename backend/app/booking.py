from app.agent_service import AgentService
from enums.booking_status import BookingStatus
from app.services import Services
from app.booking_sales import BookingSales


class Booking(AgentService, Services):
    def __init__(self, agent_id: str):
        super().__init__()
        self.__service_type = 'booking'
        self.__booking_id = ''
        self.__agent_id = agent_id
        self.__booking_placed = ''
        self.__booking_date = ""
        self.__itinerary_id = ''
        self.__total_commission = 0.0
        self.__total_price = 0.0
        self.__status = BookingStatus.PAYMENT_DUE.value
        self.__payment_type = ""
        self.__booking_sales = BookingSales()
        self.__client_info = {
            "name": "",
            "phone_number": "",
            "email": "",
            "age": 0
        }

    def get_type(self):
        return self.__service_type

    def set_booking_id(self, b_id: str):
        self.__booking_id = b_id

    def get_booking_id(self):
        return self.__booking_id

    def set_agent_id(self, agent_id: str):
        self.__agent_id = agent_id

    def get_agent_id(self):
        return self.__agent_id

    def set_booking_date(self, date):
        self.__booking_date = date

    def get_booking_date(self):
        return self.__booking_date

    def set_itinerary_id(self, i_id: str):
        self.__itinerary_id = i_id

    def get_itinerary_id(self):
        return self.__itinerary_id

    def set_agent_commissions(self, commissions):
        self.__total_commission = commissions

    def get_agent_commissions(self):
        return self.__total_commission

    def set_total_price(self, price):
        self.__total_price = price

    def get_total_price(self):
        return self.__total_price

    def set_client_info(self, client_details: dict):
        self.__client_info = client_details

    def get_client_info(self):
        return self.__client_info

    def update_client_info(self, details: dict):
        self.__client_info.update(details)

    def set_payment_type(self, p_type: str):
        self.__payment_type = p_type
        self.__status = BookingStatus.PAID.value

    def get_payment_type(self):
        return self.__payment_type

    def get_status(self):
        return self.__status

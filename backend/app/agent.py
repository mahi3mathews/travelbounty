from app.users import Users
from enums.roles import Roles
from app.service_factory import ServiceFactory
from app.payment import Payment


class Agent(Users):
    def __init__(self):
        super().__init__(Roles.AGENT.value)
        self.__service = None
        self.__booking_count = 0
        self.__itinerary_count = 0
        self.__commissions_earned = [{}]
        self.__payments = Payment()

    def set_factory_service(self):
        self.__service = ServiceFactory(self.get_user_id())

    def get_factory_service(self):
        return self.__service

    def set_itinerary_count(self, count: int):
        self.__itinerary_count = count

    def get_itinerary_count(self):
        return self.__itinerary_count

    def set_booking_count(self, count: int):
        self.__booking_count = count

    def get_booking_count(self):
        return self.__booking_count

    def set_commissions(self, commissions: list):
        self.__commissions_earned = commissions

    def get_commissions(self):
        return self.__commissions_earned

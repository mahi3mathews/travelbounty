from app.users import Users
from enums.roles import Roles
from app.service_factory import ServiceFactory
from app.travel_service import TravelService


class Admin(Users):

    def __init__(self):
        super().__init__(Roles.ADMIN.value)
        self.__all_travel_services = list
        self.__travel_service = TravelService()
        self.__service = None

    def set_factory_service(self):
        self.__service = ServiceFactory(self.get_user_id())

    def get_factory_service(self):
        return self.__service

    def set_all_travel_services(self, services: list):
        self.__all_travel_services = services

    def get_all_travel_services(self):
        return self.__all_travel_services

    def get_travel_service(self):
        return self.__travel_service

from app.travel_service import TravelService
from typing import List
from app.agent_service import AgentService
from app.services import Services


class Itinerary(AgentService, Services):

    def __init__(self, agent_id):
        super().__init__()
        self.__service_type = "itinerary"
        self.__itinerary_id = ''
        self.__agent_id = agent_id
        self.__services = []
        self.__total_price = 0.0
        self.__name = ""
        self.__description = "",
        self.__commission = 0.0

    def get_type(self):
        return self.__service_type

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_description(self, desc: str):
        self.__description = desc

    def get_description(self):
        return self.__description

    def set_itinerary_id(self, i_id: str):
        self.__itinerary_id = i_id

    def get_itinerary_id(self):
        return self.__itinerary_id

    def set_agent(self, agent_id: str):
        self.__agent_id = agent_id

    def get_agent(self):
        return self.__agent_id

    def set_travel_services(self, services: List[TravelService]):
        self.__services = services

    def add_travel_service(self):
        self.__services.append(TravelService())

    def get_travel_services(self):
        return self.__services

    def set_total_price(self, price: float):
        self.__total_price = price

    def get_total_price(self):
        return self.__total_price

    def set_travel_service_commission(self, commission):
        self.__commission = commission

    def get_travel_service_commission(self):
        return self.__commission

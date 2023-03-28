from app.booking import Booking
from app.itinerary import Itinerary


class ServiceFactory:
    def __init__(self, agent_id: str):
        self.__service = None
        self.__agent_id = agent_id

    def set_agent_id(self, agent_id):
        self.__agent_id = agent_id

    def get_agent_id(self):
        return self.__agent_id

    def get_service(self, service_name: str):
        if service_name is not None:
            if service_name.lower() == "booking":
                self.__service = Booking(self.__agent_id)
            elif service_name.lower() == "itinerary":
                self.__service = Itinerary(self.__agent_id)
            else:
                self.__service = None
        return self.__service


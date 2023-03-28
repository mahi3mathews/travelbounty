from enums.service_types import ServiceTypes


class TravelService:

    def __init__(self):
        self.__name = ''
        self.__type = ''
        self.__price = 0.0
        self.__details = {}
        self.__admin_id = ''

    def set_name(self, name: str):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_type(self, s_type: ServiceTypes):
        self.__type = s_type

    def get_type(self):
        return self.__type

    def set_price(self, price: str):
        self.__price = price

    def get_price(self):
        return self.__price

    def set_details(self, details: str):
        self.__details = details

    def get_details(self):
        return self.__details

    def update_details(self, new_details: dict):
        self.__details.update(new_details)

from app.service_sales import ServiceSales


class Services:
    def __init__(self):
        self.__bookings = []
        self.__travel_services = []

    def set_services(self, services):
        self.__travel_services = services

    def set_bookings(self, bookings):
        self.__bookings = bookings

    def calculate_sale_commission(self, service_id_list):
        return ServiceSales.sale_commission(self.__travel_services, service_id_list)

    def calculate_total_sales(self, service_id_list: list):
        return ServiceSales.total_sales(self.__travel_services, service_id_list)

    def calculate_sale_by_agent(self, agents):
        return ServiceSales.services_sold(self.__bookings, self.__travel_services, agents)

    def calculate_all_services_sale(self):
        return ServiceSales.all_services_sale(self.__bookings, self.__travel_services)

    def calculate_all_services_commission(self):
        return ServiceSales.all_services_commission(self.__bookings, self.__travel_services)


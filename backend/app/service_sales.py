from flask_pymongo import ObjectId


class ServiceSales:

    @staticmethod
    def total_sales(services, service_id_list):
        total_price = 0.0
        for service_id in service_id_list:
            service = [x for x in services if x["_id"] == ObjectId(service_id)]
            total_price = total_price + service[0]["price"]
        return total_price

    @staticmethod
    def sale_commission(services, service_id_list):
        total_commission = 0.0
        for service_id in service_id_list:
            service = [x for x in services if x["_id"] == ObjectId(service_id)]
            total_commission = total_commission + service[0]["commission"]
        return total_commission

    @staticmethod
    def services_sold(bookings, services, agents):
        output = {}
        agents_details = {}
        for booking in bookings:
            agent = [x for x in agents if x["_id"] == ObjectId(booking["agent_id"])]
            agents_details[booking["agent_id"]] = agent[0]["name"]
            service_list = []
            for service_data in services:
                if str(ObjectId(service_data["_id"])) in booking["services"]:
                    service_list.append(service_data)
            if booking["agent_id"] not in output:
                output[booking["agent_id"]] = {}
            for service_info in service_list:
                if str(service_info["_id"]) not in output[booking["agent_id"]]:
                    output[booking["agent_id"]][str(service_info["_id"])] = 0.0
                output[booking["agent_id"]][str(service_info["_id"])] += service_info["price"]

        result = []
        for agent_id, service_totals in output.items():
            result.append({agents_details[agent_id]: service_totals})
        return result

    @staticmethod
    def all_services_sale(bookings, services):
        output = {}
        for booking in bookings:
            service_list = []
            for service_data in services:
                if str(ObjectId(service_data["_id"])) in booking["services"]:
                    service_list.append(service_data)
            for service_info in service_list:
                if str(service_info["_id"]) not in output:
                    output[str(service_info["_id"])] = 0.0
                output[str(service_info["_id"])] += service_info["price"]

        return output

    @staticmethod
    def all_services_commission(bookings, services):
        output = {}
        for booking in bookings:
            service_list = []
            for service_data in services:
                if str(ObjectId(service_data["_id"])) in booking["services"]:
                    service_list.append(service_data)
            for service_info in service_list:
                if str(service_info["_id"]) not in output:
                    output[str(service_info["_id"])] = 0.0
                output[str(service_info["_id"])] += service_info["commission"]

        return output

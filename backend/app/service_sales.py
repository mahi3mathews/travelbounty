from flask_pymongo import ObjectId


class ServiceSales:
    # total sale based on list of services
    @staticmethod
    def total_sales(services, service_id_list):
        total_price = 0.0
        for service_id in service_id_list:
            service_data = None
            for service in services:
                if service["_id"] == ObjectId(service_id):
                    service_data = service
            total_price = total_price + service_data["price"]
        return round(total_price, 2)

    # total commission based on list of services
    @staticmethod
    def sale_commission(services, service_id_list):
        total_commission = 0.0
        for service_id in service_id_list:
            service = [x for x in services if x["_id"] == ObjectId(service_id)]
            total_commission = total_commission + service[0]["commission"]
        return round(total_commission, 2)

    # total sale of services of agents
    @staticmethod
    def services_sold_by_agents(bookings, services, agents):
        output = {}
        agents_details = {}
        for booking in bookings:
            agent = []
            for agent_info in agents:
                if str(ObjectId(agent_info["_id"])) in booking["agent_id"]:
                    agent.append(agent_info)
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
                output[booking["agent_id"]][str(service_info["_id"])] = round(service_info["price"] +
                                                                              output[booking["agent_id"]]
                                                                              [str(service_info["_id"])], 2)

        result = []
        for agent_id, service_totals in output.items():
            result.append({agents_details[agent_id]: service_totals})
        return result

    # all services with total sale
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
                output[str(service_info["_id"])] = round(service_info["price"] + output[str(service_info["_id"])], 2)

        return output

    # all services with total commission
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

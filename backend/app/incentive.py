from app.payment import Payment


class Incentive(Payment):
    def __init__(self):
        super().__init__()
        self.__agent_id = ''
        self.__amount = ''
        self.__payment_date = ''
        self.__type = ''
        self.__status = ''
        self.__details = {}

    def set_agent_id(self, agent_id):
        self.__agent_id = agent_id

    def get_agent_id(self):
        return self.__agent_id

    def set_amount(self, amount):
        self.__amount = amount

    def get_amount(self):
        return self.__amount

    def set_payment_date(self, date):
        self.__payment_date = date

    def get_payment_date(self):
        return self.__payment_date

    def set_type(self, p_type):
        self.__type = p_type

    def get_type(self):
        return self.__type

    def set_status(self, status):
        self.__status = status

    def get_status(self):
        return self.__status

    def get_details(self):
        return self.__details

    def set_details(self, details):
        return self.__details


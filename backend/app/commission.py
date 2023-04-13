from app.payment import Payment


class Commission(Payment):
    """
      Represents a commission payment made to an agent.

      Inherits from Payment class. Includes attributes for agent ID, payment amount,
      payment date, payment type, payment status, and creator details.

      Attributes:
      ----------
      __agent_id: str
          The ID of the agent who received the commission payment.
      __amount: float
          The amount of the commission payment.
      __payment_date: str
          The date when the commission payment was made.
      __type: str
          The type of the commission payment.
      __status: str
          The status of the commission payment.
      __created_by: dict
          The details of the creator of the commission payment, including name and ID.

      Methods:
      -------
      set_agent_id(agent_id: str) -> None:
          Sets the agent ID attribute to the specified value.
      get_agent_id() -> str:
          Returns the agent ID attribute.
      set_amount(amount: float) -> None:
          Sets the amount attribute to the specified value.
      get_amount() -> float:
          Returns the amount attribute.
      set_payment_date(date: str) -> None:
          Sets the payment date attribute to the specified value.
      get_payment_date() -> str:
          Returns the payment date attribute.
      set_type(p_type: str) -> None:
          Sets the payment type attribute to the specified value.
      get_type() -> str:
          Returns the payment type attribute.
      set_status(status: str) -> None:
          Sets the payment status attribute to the specified value.
      get_status() -> str:
          Returns the payment status attribute.
      set_created_by(details: dict) -> None:
          Sets the creator details attribute to the specified dictionary.
      get_created_by() -> dict:
          Returns the creator details attribute.
      """
    def __init__(self):
        super().__init__()
        self.__agent_id = ''
        self.__amount = ''
        self.__payment_date = ''
        self.__type = ''
        self.__status = ''
        self.__created_by = {}

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

    def get_created_by(self):
        return self.__created_by

    def set_created_by(self, details):
        self.__created_by = details

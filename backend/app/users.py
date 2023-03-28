class Users:
    def __init__(self, user_role):
        self.__user_id = ""
        self.__email = ""
        self.__password = ""
        self.__name = ""
        self.__role = user_role

    def set_user_id(self, user_id: str):
        self.__user_id = user_id

    def get_user_id(self):
        return self.__user_id

    def set_email(self, email: str):
        self.__email = email

    def get_email(self):
        return self.__email

    def set_password(self, pwd: str):
        self.__password = pwd

    def get_password(self):
        return self.__password

    def set_name(self, name: str):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_role(self, role: ""):
        self.__role = role

    def get_role(self):
        return self.__role

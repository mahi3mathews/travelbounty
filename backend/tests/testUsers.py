import unittest
from app.users import Users
from enums.roles import Roles


class TestUsers(unittest.TestCase):

    def test_set_name(self):
        b = Users(Roles.AGENT.value)
        b.set_name("Larry")
        self.assertEqual(b.get_name(), "Larry")
        self.assertNotEqual(b.get_name(), "Adam")

    def test_set_user_agent_role(self):
        b = Users(Roles.AGENT.value)
        self.assertEqual(b.get_role(), Roles.AGENT.value)

    def test_set_user_admin_role(self):
        b = Users(Roles.ADMIN.value)
        self.assertEqual(b.get_role(), Roles.ADMIN.value)

    def test_set_user_agent_id(self):
        b = Users(Roles.AGENT.value)
        b.set_user_id("id1")
        self.assertEqual(b.get_user_id(), "id1")


    def test_user_email_pwd(self):
        b = Users(Roles.AGENT.value)
        b.set_email("a@g.com")
        b.set_password("a_231")
        self.assertEqual(b.get_email(), "a@g.com")
        self.assertEqual(b.get_password(), "a_231")



import unittest

from penote.service import session


class SessionTestCase(unittest.TestCase):
    def test_exists_by_user_name(self):
        user_name = 'hello'
        self.assertFalse(session.exists_by_user_name(user_name))

    def test_invalidate_by_user_name(self):
        user_name = 'hello'
        session.invalidate_by_user_name(user_name)
        self.assertFalse(session.exists_by_user_name(user_name))

    def test_login(self):
        json = {'user_name': 'hello', 'password': '123456'}
        ret = session.login(json)
        print(ret)

    def test_logout(self):
        id = '2854689e-ee94-4a3d-b924-3f78e75c4e97'
        ret = session.logout(id)
        print(ret)

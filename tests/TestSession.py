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
        ret = session.sign_in(json)
        print(ret)

    def test_logout(self):
        id = '2854689e-ee94-4a3d-b924-3f78e75c4e97'
        ret = session.signout(id)
        print(ret)

    def test_get_user_id_by_id(self):
        s_id = '12eea966-3bc3-4686-a657-495da079bad8'
        user_id = session.get_user_id_by_id(s_id)
        self.assertEqual(user_id, 'c925389a-642d-4bfb-9478-6472bc2aa92f')

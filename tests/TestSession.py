import unittest

from penote.service import session


class SessionTestCase(unittest.TestCase):
    def test_exists_by_user_name(self):
        user_name = 'hello'
        self.assertFalse(session.exists_by_user_name(user_name))

    def test_invalidate_by_user_id(self):
        user_id = '3ccb0d3e-832d-418e-8aae-de75f2d2f208'
        session.invalidate_by_user_id(user_id)
        self.assertFalse(session.exists_by_user_name('hello'))

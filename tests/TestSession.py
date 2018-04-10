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

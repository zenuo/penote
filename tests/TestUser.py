import unittest

from penote.service import user


class UserTestCase(unittest.TestCase):
    def test_exists_by_name(self):
        self.assertTrue(user.exists_by_name('hello'))

    def test_exists_by_id(self):
        self.assertTrue(user.exists_by_id('3ccb0d3e-832d-418e-8aae-de75f2d2f208'))

    def test_check_password(self):
        result = user.check_password('hello', '123456')
        self.assertTrue(result[0])

    def test_invalidate(self):
        id = '3ccb0d3e-832d-418e-8aae-de75f2d2f208'
        user.invalidate(id, None)
        self.assertFalse(user.exists_by_id(id, 0))

    def test_validate(self):
        id = '3ccb0d3e-832d-418e-8aae-de75f2d2f208'
        user.validate(id, None)
        self.assertTrue(user.exists_by_id(id, 0))

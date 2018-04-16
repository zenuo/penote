import unittest

from penote.service import category


class TestCategory(unittest.TestCase):
    def test_create(self):
        json = {'session': '12eea966-3bc3-4686-a657-495da079bad8', 'name': '技术'}
        ret = category.create(json)
        print(ret)

    def test_exists_by_user_id_and_name(self):
        user_id = 'c925389a-642d-4bfb-9478-6472bc2aa92f'
        name = '技术'
        self.assertIsNotNone(category.get_by_user_id_and_name(user_id, name))

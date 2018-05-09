from unittest import TestCase

from penote.service import post


class PostTestCase(TestCase):
    def test_get_all(self):
        l = post.get_all()
        print(len(l))

    def test_get_list_by_title(self):
        l = post.get_list_by_title('春')
        print(len(l))

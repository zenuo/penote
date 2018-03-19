import unittest
from penote.rectangle import Rectangle


class MyTestCase(unittest.TestCase):
    def test_overlapping(self):
        # 重叠
        r1 = Rectangle(30, 20, 30, 50)
        r2 = Rectangle(50, 50, 30, 40)
        self.assertTrue(r1.overlapping(r2))
        self.assertTrue(r2.overlapping(r1))
        # 自己与自己重叠
        self.assertTrue(r1.overlapping(r1))
        self.assertTrue(r2.overlapping(r2))
        # 不相交
        r3 = Rectangle(10, 10, 10, 10)
        r4 = Rectangle(0, 0, 0, 0)
        self.assertFalse(r3.overlapping(r4))
        # 相交
        r5 = Rectangle(20, 30, 60, 30)
        r6 = Rectangle(40, 10, 20, 70)
        self.assertTrue(r5.overlapping(r6))

    def test_merge_in_place(self):
        """
        测试原地合并矩形
        :return:
        """
        a = Rectangle(3, 2, 3, 5)
        b = Rectangle(5, 5, 3, 4)
        a.merge_in_place(b)
        self.assertEqual(a, Rectangle(3, 2, 5, 7))


if __name__ == '__main__':
    unittest.main()

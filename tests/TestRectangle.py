import unittest

import numpy as np
from penote.klass import Rectangle

from penote import utils


class MyTestCase(unittest.TestCase):
    def test_overlapping(self):
        r1 = Rectangle(30, 20, 30, 50)
        r2 = Rectangle(50, 50, 30, 40)
        self.assertTrue(r1.overlapping(r2))
        self.assertTrue(r2.overlapping(r1))
        self.assertTrue(r1.overlapping(r1))
        self.assertTrue(r2.overlapping(r2))
        r3 = Rectangle(10, 10, 10, 10)
        r4 = Rectangle(0, 0, 0, 0)
        self.assertFalse(r3.overlapping(r4))
        r5 = Rectangle(20, 30, 60, 30)
        r6 = Rectangle(40, 10, 20, 70)
        self.assertTrue(r5.overlapping(r6))
        r7 = Rectangle(0, 0, 100, 100)
        r8 = Rectangle(10, 10, 10, 10)
        self.assertTrue(r7.overlapping(r8))
        self.assertTrue(r8.overlapping(r7))

    def test_merge_in_place(self):
        """
        测试原地合并矩形
        """
        r1 = Rectangle(3, 2, 3, 5)
        r2 = Rectangle(5, 5, 3, 4)
        r1.merge_in_place(r2)
        self.assertEqual(r1, Rectangle(3, 2, 5, 7))
        r3 = Rectangle(0, 0, 100, 100)
        r4 = Rectangle(10, 10, 10, 10)
        r4.merge_in_place(r3)
        self.assertEqual(r4, Rectangle(0, 0, 100, 100))
        r5 = Rectangle(0, 0, 100, 100)
        r6 = Rectangle(10, 10, 10, 10)
        r6.merge_in_place(r5)
        self.assertEqual(r6, Rectangle(0, 0, 100, 100))

    def test_horizontal_blank_lines(self):
        a = np.array(
            [[0, 0, 1],
             [0, 0, 0],
             [0, 0, 1],
             [0, 0, 0]],
            dtype=np.uint8)
        lines = utils.horizontal_blank_lines(a)
        self.assertEqual(lines, list([1, 3]))


if __name__ == '__main__':
    unittest.main()

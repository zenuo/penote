from typing import Tuple


class Rectangle:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        return '%d, %d, %d, %d' % (self.x, self.y, self.w, self.h)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.x == other.x and \
               self.y == other.y and \
               self.w == other.w and \
               self.h == other.h

    @staticmethod
    def x_position(cls):
        return cls.x

    @staticmethod
    def y_position(cls):
        return cls.y

    def points(self):
        """
        获取四个顶点的坐标元组
        :return: 四个顶点的坐标元组
        """
        return (self.x, self.y), \
               (self.x, self.y + self.h), \
               (self.x + self.w, self.y), \
               (self.x + self.w, self.y + self.h)

    def point_in(self, p: Tuple[int, int]):
        """
        判断某个点是否在本矩形内，包含边界
        :param p: 需要判断的点
        :return: 若在，返回True，否则返回False
        """
        return self.x <= p[0] <= self.x + self.w and self.y <= p[1] <= self.y + self.h

    def merge_in_place(self, other):
        """
        原地合并矩形
        :param other: 需要合并的矩形
        :return: None
        """
        # 创建临时矩形，合并完成后更新到self
        merged = Rectangle()
        # 左下点横坐标
        merged.x = min(self.x, other.x)
        # 左下点纵坐标
        merged.y = min(self.y, other.y)
        # 宽度
        merged.w = max(self.x + self.w, other.x + other.w) - merged.x
        # 高度
        merged.h = max(self.y + self.h, other.y + other.h) - merged.y
        # 更新到self
        self.x = merged.x
        self.y = merged.y
        self.w = merged.w
        self.h = merged.h

    def overlapping(self, other) -> bool:
        """
        判断两个矩形是否重叠
        :param other: 需要判断的矩形
        :return: 若重叠，返回True，否则返回False
        """
        # 纵向重叠
        vertical_overlapping = self.y <= other.y <= self.y + self.h or \
                               self.y <= other.y + other.h <= self.y + self.h or \
                               (other.y <= self.y <= other.y + other.h and
                                other.y <= self.y + self.h <= other.y + other.h)
        # 横向重叠
        horizontal_overlapping = self.x <= other.x <= self.x + self.w or \
                                 self.x <= other.x + other.w <= self.x + self.w or \
                                 (other.x <= self.x <= other.x + other.w and
                                  other.x <= self.x + self.w <= other.x + other.w)
        overlapping = vertical_overlapping and horizontal_overlapping
        # 绘图
        # image = np.zeros(506 * 506 * 3, dtype=np.uint8).reshape((506, 506, 3))
        # cv2.rectangle(image, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 0, 255), 1)
        # cv2.rectangle(image, (other.x, other.y), (other.x + other.w, other.y + other.h), (0, 255, 0), 1)
        # cv2.imshow(str(overlapping) + str(time.time()), image)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        return overlapping

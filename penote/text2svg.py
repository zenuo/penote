import cv2
import numpy as np
from typing import List
from penote.rectangle import Rectangle
from collections import deque


def get_bounding_rectangles(source: np.ndarray) -> List[Rectangle]:
    """
    返回边界矩形列表
    :param source: 原图
    :return: 边界矩形列表
    """
    # 反相
    inverted_grayscale = 255 - cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    # 二值化
    _, binary = cv2.threshold(inverted_grayscale, 180, 255, cv2.THRESH_OTSU)
    binary_rgb = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    # 轮廓
    _, contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 返回矩形列表
    rectangles = list(Rectangle(*cv2.boundingRect(c)) for c in contours)
    rectangles = combine_overlapping_rectangles(rectangles)
    for r in rectangles:
        cv2.rectangle(binary_rgb, (r.x, r.y), (r.x + r.w, r.y + r.h), (0, 0, 255), 1)
    cv2.imwrite("../tests/hello_world_hand_writen_with_bounding_rectangles.jpg", binary_rgb)
    return rectangles


def combine_overlapping_rectangles(source_list: List[Rectangle]) -> List[Rectangle]:
    """
    合并重叠的矩形
    :param source_list: 输入矩形列表
    :return: 合并相交的矩形后的矩形列表
    """
    # 以矩形的最大纵坐标值排序
    source_list.sort()
    # 源队列
    source_queue = deque(source_list)
    # 结果列表
    result_list = list()
    # 遍历源队列
    while len(source_queue) != 0:
        current: Rectangle = source_queue.popleft()
        temp_queue = deque()
        overlapping: bool = False
        while len(source_queue) != 0:
            temp_r: Rectangle = source_queue.popleft()
            if current.overlapping(temp_r):
                overlapping = True
                current.merge_in_place(temp_r)
            else:
                temp_queue.append(temp_r)
        if overlapping:
            temp_queue.appendleft(current)
        else:
            result_list.append(current)
        source_queue = temp_queue.copy()
        temp_queue.clear()
    return result_list


if __name__ == '__main__':
    # 灰度图像
    image = cv2.imread('../tests/hello_world_hand_writen.jpg', cv2.IMREAD_REDUCED_COLOR_2)
    # 降噪
    denoising = cv2.fastNlMeansDenoising(image)
    bounding_rectangles = get_bounding_rectangles(denoising)
    print(len(bounding_rectangles))
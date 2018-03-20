from collections import deque
from typing import List, Tuple

import cv2
import numpy as np

from penote.rectangle import Rectangle


def bounding_rectangles(source: np.ndarray):
    """
    返回边界矩形列表
    :param source: 原图
    :return: 二值化图像，边界矩形列表
    """
    # 反相
    inverted_grayscale = 255 - source
    # 二值化
    _, binary = cv2.threshold(inverted_grayscale, 180, 255, cv2.THRESH_OTSU)
    # 彩色的二值化图像，便于绘制有色矩形
    binary_rgb = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    # 轮廓
    _, contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 合并重叠的矩形后返回列表
    rectangles = combine_overlapping_rectangles(list(Rectangle(*cv2.boundingRect(c)) for c in contours))
    # for r in rectangles:
    #     cv2.rectangle(binary_rgb, (r.x, r.y), (r.x + r.w, r.y + r.h), (0, 0, 255), 1)
    #     cv2.putText(binary_rgb, str(r), (r.x, r.y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1)
    # cv2.imwrite("../tests/hello_world_hand_writen_with_bounding_rectangles.jpg", binary_rgb)
    return binary, rectangles


def combine_overlapping_rectangles(source_list: List[Rectangle]) -> List[Rectangle]:
    """
    合并重叠的矩形
    :param source_list: 输入矩形列表
    :return: 合并后的矩形列表
    """
    # 源队列
    source_queue = deque(source_list)
    # 结果列表
    result_list = list()
    # 遍历源队列
    while len(source_queue) != 0:
        # 取出队首
        current: Rectangle = source_queue.popleft()
        # 暂存队列
        temp_queue = deque()
        # 是否存在重叠
        overlapping: bool = False
        # 遍历余下队列
        while len(source_queue) != 0:
            # 暂存矩形
            temp_r: Rectangle = source_queue.popleft()
            # 判断是否与current重叠
            if current.overlapping(temp_r):
                # 若重叠，则置overlapping为True
                overlapping = True
                # 原地合并temp_r到current
                current.merge_in_place(temp_r)
            else:
                # 若不重叠，加入暂存队列
                temp_queue.append(temp_r)
        if overlapping:
            # 若在此次遍历中发生重叠，将current加入暂存队列
            temp_queue.appendleft(current)
        else:
            # 若无重叠，则表示current已经合并完成，加入结果列表
            result_list.append(current)
        # 将暂存队列拷贝至源队列
        source_queue = temp_queue.copy()
        # 清空暂存队列
        temp_queue.clear()
    return result_list


def rowing(rectangles: List[Rectangle], shape: Tuple[int, int]) -> List[List[Rectangle]]:
    """
    将矩形列表分行，返回二维列表，模拟其在文本上的位置
    :param rectangles: 输入矩形列表
    :param shape: 图像（灰度图像）的形状
    :return: 二维矩形列表
    """
    # 以y位置排序
    rectangles.sort(key=Rectangle.y_position)
    # 图像宽度
    width: int = shape[1]
    # 结果列表
    result_list = list()
    # 暂存列表
    temp_list = list()
    # 遍历矩形列表
    for r in rectangles:
        if r.x + r.y < width:
            temp_list.append(r)
        else:
            result_list.append(temp_list.copy())
            temp_list.clear()
            temp_list.append(r)
    # 将暂存列表加入结果列表
    result_list.append(temp_list)
    # 遍历结果列表，以x位置排序
    for l in result_list:
        l.sort(key=Rectangle.x_position)
    # 返回
    return result_list


if __name__ == '__main__':
    # 灰度图像
    grayscale: np.ndarray = cv2.imread('../tests/hello_world_hand_writen.jpg', cv2.IMREAD_GRAYSCALE)
    # 降噪
    denoising: np.ndarray = cv2.fastNlMeansDenoising(grayscale)
    # 获取二值化图像和边界矩形列表
    binary, rectangles = bounding_rectangles(denoising)
    # 分行
    rows = rowing(rectangles, denoising.shape)
    # 行和列
    row_count = 1
    column_count = 1
    # 遍历
    for row in rows:
        for rect in row:
            roi = binary[rect.y:rect.y + rect.h, rect.x:rect.x + rect.w]
            cv2.imshow("Row:%d Column:%d" % (row_count, column_count), roi)
            column_count += 1
        row_count += 1
        column_count = 1
    cv2.waitKey()

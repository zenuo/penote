import logging
import os
import statistics
import subprocess
import uuid
from collections import deque

import cv2
import numpy as np

from penote import config
from penote.klass import Rectangle

# 将bmp文件转为svg的命令
CMD_BMP2SVG = 'potrace %s -s -i -o %s'
# 日志
LOGGER = logging.getLogger(__name__)
# 获取配置
CONFIG_JSON = config.get()


def bounding_rectangles(source):
    """
    返回边界矩形列表
    :param source: 原图
    :return: 边界点列表，边界矩形列表
    """
    # 反相
    inverted_grayscale = 255 - source
    # 二值化
    _, binary = cv2.threshold(inverted_grayscale, 180, 255, cv2.THRESH_OTSU)
    # 彩色的二值化图像，便于绘制有色矩形
    # binary_rgb = np.zeros(source.shape)
    # 所有轮廓
    _, all_contours, _ = cv2.findContours(
        binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 合并重叠的矩形后返回列表
    rectangles = combine_overlapping_rectangles(
        list(Rectangle(*cv2.boundingRect(c), c) for c in all_contours))
    # for r in rectangles:
    #     绘制边界矩形
    #     cv2.rectangle(binary_rgb, (r.x, r.y), (r.x + r.w, r.y + r.h), (0, 0, 255), 1)
    #     简化近似轮廓
    #     smoothed_contours = list(cv2.approxPolyDP(c, 0.005 * cv2.arcLength(c, True), True) for c in r.cl)
    #     print("未处理的轮廓点数：%d\n平滑处理后的轮廓点数：%d" % (count_points(r.cl), count_points(smoothed_contours)))
    #     绘制轮廓
    # cv2.drawContours(binary_rgb, r.cl, -1, (255, 255, 255), 1)
    #     cv2.putText(binary_rgb, str(r), (r.x, r.y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1)
    # cv2.imwrite("../tests/field_with_contours.jpg", binary_rgb)
    return binary, rectangles


def combine_overlapping_rectangles(source_list):
    """
    合并重叠的矩形
    :param source_list: 输入矩形列表
    :return: 合并后的矩形列表
    """
    source_list.sort(key=Rectangle.y_position)
    # 源队列
    source_queue = deque(source_list)
    # 结果列表
    result_list = list()
    # 遍历源队列
    while not source_queue:
        # 取出队首
        current = source_queue.popleft()
        # 暂存队列
        temp_queue = deque()
        # 是否存在重叠
        overlapping = False
        # 遍历余下队列
        while not source_queue:
            # 暂存矩形
            temp_r = source_queue.popleft()
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
    # 返回
    return result_list


def horizontal_blank_lines(binary):
    """
    获取所有水平的空白线的纵坐标，对相邻的空白线集合取其中值
    :param binary: 二值化图像
    :return: 所有水平的空白线的纵坐标
    """
    # 高度
    height = binary.shape[0]
    # 结果列表
    result_list = []
    # 暂存列表
    temp_list = []
    # 遍历每一行像素
    for i in range(height):
        # 取一行像素
        line: np.ndarray = binary[i]
        # 若此行为空白
        if not line.any():
            temp_list.append(i)
        # 若此行不为空白且暂存列表不为空
        elif not temp_list:
            # 求中值并添加到结果列表
            result_list.append(int(statistics.median(temp_list)))
            # 清空暂存列表
            temp_list.clear()
    # 求中值并添加到结果列表
    result_list.append(int(statistics.median(temp_list)))
    # 若图像第一行为空白，不返回第一个元素
    if not binary[0].any():
        return result_list[1:]
    else:
        return result_list


def rowing(rectangles, lines):
    """
    将矩形列表分行，返回二维列表，模拟其在文本上的位置
    :param rectangles: 输入矩形列表
    :param lines: 空白的水平线
    :return: 二维矩形列表
    """
    source_queue = deque(rectangles)
    # 结果列表
    result_list = list()
    # 暂存列表
    temp_list = list()
    # 遍历矩形列表
    for l in lines:
        while not source_queue:
            r: Rectangle = source_queue.popleft()
            if r.y + r.h < l:
                temp_list.append(r)
            elif not temp_list:
                result_list.append(temp_list.copy())
                temp_list.clear()
                temp_list.append(r)
                break
            else:
                source_queue.appendleft(r)
    # 将暂存列表加入结果列表
    result_list.append(temp_list)
    # 遍历结果列表，以x位置排序
    for l in result_list:
        l.sort(key=Rectangle.x_position)
        # l.sort(key=lambda a: a.x)
    # 返回
    return result_list


def jpg2svg(photo_path):
    LOGGER.info('jpg2svg: %s', photo_path)
    # 灰度图像
    grayscale: np.ndarray = cv2.imread(
        photo_path,
        cv2.IMREAD_GRAYSCALE
    )
    # 降噪
    denoising: np.ndarray = cv2.fastNlMeansDenoising(grayscale)
    # 获取二值化图像和边界矩形列表
    binary, rectangles = bounding_rectangles(denoising)
    # 水平空白行列表
    blank_lines = horizontal_blank_lines(binary)
    # 分行
    rows = rowing(rectangles, blank_lines)
    # UUID
    uuid_str = str(uuid.uuid4())
    # 行和列
    row_count = 1
    column_count = 1
    # 遍历
    for row in rows:
        for rect in row:
            # 切片以获得文字的位图
            character = binary[rect.y - 1:rect.y +
                               rect.h + 1, rect.x - 1:rect.x + rect.w + 1]
            # bmp文件路径
            bmp_path = '%s%s%s_%d_%d.bmp' % (
                CONFIG_JSON['temp_path'], os.sep, uuid_str, row_count, column_count)
            # svg文件路径
            svg_path = '%s%s%s_%d_%d.svg' % (
                CONFIG_JSON['svg_path'], os.sep, uuid_str, row_count, column_count)
            # 将bmp文件写入暂存
            cv2.imwrite(bmp_path, character)
            # 转换bmp到svg
            cmd = (CMD_BMP2SVG % (bmp_path, svg_path)).split()
            subprocess.call(cmd)
            # 增加列计数
            column_count += 1
        # 增加列计数
        row_count += 1
        # 重置列计数
        column_count = 1
    LOGGER.info(
        'photo "%s" to %s, %d rows and %d columns',
        photo_path,
        uuid_str,
        row_count,
        column_count
    )


if __name__ == '__main__':
    jpg2svg('/home/yuanzhen/project/penote/tests/listen.jpg')

import logging
import statistics
import subprocess
import uuid
from collections import deque

import cv2
import numpy as np

from .config import get_config
from .data import SESSION_MAKER
from .models import Character, Paragraph, Rectangle

# 将bmp文件转为svg的命令
__CMD_BMP2SVG = 'potrace %s -s -i -o %s'
# 日志
LOGGER = logging.getLogger(__name__)


def bounding_rectangles(source):
    """
    返回边界矩形列表
    :param source: 原图
    :return: 边界点列表，边界矩形列表
    """
    # 反相
    inverted_grayscale = 255 - source
    # 二值化
    _, binary = cv2.threshold(inverted_grayscale, 0, 255, cv2.THRESH_OTSU)
    # 彩色的二值化图像，便于绘制有色矩形
    binary_rgb = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    # 所有轮廓
    _, all_contours, _ = cv2.findContours(
        binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 合并重叠的矩形后返回列表
    rectangles = combine_overlapping_rectangles(
        list(Rectangle(*cv2.boundingRect(c), c) for c in all_contours))
    for r in rectangles:
        # 绘制边界矩形
        cv2.rectangle(binary_rgb, (r.x, r.y), (r.x + r.w, r.y + r.h), (255, 255, 255), 1)
        # 绘制轮廓
        # cv2.drawContours(binary_rgb, r.cl, -1, (255, 255, 255), 1)
        # cv2.putText(binary_rgb, str(r), (r.x, r.y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255, 255, 255), 1)
    # cv2.imwrite("../tests/rectangles.jpg", binary_rgb)
    return binary, rectangles, binary_rgb


def combine_overlapping_rectangles(source_list):
    """
    合并重叠的矩形
    :param source_list: 输入矩形列表
    :return: 合并后的矩形列表
    """
    source_list.sort(key=lambda a: a.y)
    # 源队列
    source_queue = deque(source_list)
    # 结果列表
    result_list = list()
    # 遍历源队列
    while source_queue:
        # 取出队首
        current = source_queue.popleft()
        # 暂存队列
        temp_queue = deque()
        # 是否存在重叠
        overlapping = False
        # 遍历余下队列
        while source_queue:
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
        elif temp_list:
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
    result_list = []
    # 暂存列表
    temp_list = []
    # 遍历矩形列表
    for l in lines:
        while source_queue:
            r: Rectangle = source_queue.popleft()
            if r.y + r.h < l:
                temp_list.append(r)
            elif temp_list:
                temp_list.sort(key=lambda a: a.x)
                result_list.append(temp_list.copy())
                temp_list.clear()
                temp_list.append(r)
                break
            else:
                source_queue.appendleft(r)
    # 将暂存列表加入结果列表
    result_list.append(temp_list)
    # 返回
    return result_list


def photo2svg(photo_path, post_id):
    """
    照片转SVG
    :param photo_path: 照片文件的路径
    :param post_id: 文章ID
    :param sess: 会话实例
    :return: 段落ID
    """
    # 灰度图像
    grayscale: np.ndarray = cv2.imread(photo_path, cv2.IMREAD_REDUCED_GRAYSCALE_2)
    # 降噪
    denoising: np.ndarray = cv2.fastNlMeansDenoising(grayscale)
    # 获取二值化图像和边界矩形列表
    binary, rectangles, binary_rgb = bounding_rectangles(denoising)
    # 水平空白行列表
    blank_lines = horizontal_blank_lines(binary)
    # 绘制分行
    # for line in blank_lines:
    #     cv2.line(binary_rgb, (0, line), (binary_rgb.shape[0], line), (255,255,255), 1, cv2.LINE_4)
    # cv2.imwrite('../tests/line.jpg', binary_rgb)
    # 分行
    rows = rowing(rectangles, blank_lines)
    # 段落ID
    paragraph_id = str(uuid.uuid4())
    # 创建段落实例
    paragraph = Paragraph(
        id=paragraph_id,
        post_id=post_id,
        index_number=0
    )
    # 计数
    count = 0
    # 文字列表
    character_list = []
    # 遍历
    for row in rows:
        for rect in row:
            # 绘制字符顺序号
            cv2.putText(binary_rgb, str(count), (rect.x, rect.y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255, 255, 255), 1)
            # 文字ID
            character_id = str(uuid.uuid4())
            # 文字实例
            character = Character(
                id=character_id,
                paragraph_id=paragraph_id,
                index_number=count
            )
            character_list.append(character)
            # 切片，四个方向各扩大一像素
            character_slice = binary[rect.y - 1:rect.y +
                                     rect.h + 1, rect.x - 1:rect.x + rect.w + 1]
            # bmp文件路径
            bmp_path = '%s/%s.bmp' % (get_config().get('bmp_path'), character_id)
            # svg文件路径
            svg_path = '%s/%s.svg' % (get_config().get('svg_path'), character_id)
            # 将bmp文件写入暂存
            cv2.imwrite(bmp_path, character_slice)
            # 转换bmp到svg
            cmd = (__CMD_BMP2SVG % (bmp_path, svg_path)).split()
            # 执行bmp转svg，并记录其返回码，判断其是否成功执行
            ret_code = subprocess.call(cmd)
            if ret_code != 0:
                LOGGER.info('执行命令失败 "%s"', cmd)
            # 增加计数
            count += 1
    cv2.imwrite('../tests/character_order.jpg', binary_rgb)
    # 创建会话
    sess = SESSION_MAKER()
    try:
        # 持久化
        sess.add(paragraph)
        sess.add_all(character_list)
        sess.commit()
    except Exception as ex:
        LOGGER.error('图片转SVG异常', ex)
    finally:
        sess.close()
        return paragraph_id


if __name__ == '__main__':
    """ 测试方法 """
    post_id = str(uuid.uuid4())
    para_id = photo2svg(
        '/home/yz/project/penote/tests/spring_dawn.jpg',
        post_id
    )
    print('测试生成的段落ID=%s' % para_id)

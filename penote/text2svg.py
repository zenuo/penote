import cv2
import numpy as np
from collections import namedtuple

Rectangle = namedtuple('Rectangle', 'x y w h')


def get_bounding_rectangles(source: np.ndarray):
    """
    返回边界矩形列表
    :param source: 原图
    :return: 边界矩形列表
    """
    # 反相
    inverted_grayscale = 255 - cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    # 二值化
    _, binary = cv2.threshold(inverted_grayscale, 180, 255, cv2.THRESH_OTSU)
    # 轮廓
    _, contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 返回矩形列表
    rectangles = list(Rectangle(*cv2.boundingRect(c)) for c in contours)
    for x, y, w, h in rectangles:
        cv2.rectangle(source, (x, y), (x + w, y + h), (0, 0, 255), 1)
    cv2.imwrite("../tests/hello_world_hand_writen_with_bounding_rectangles.jpg", source)
    return rectangles


if __name__ == '__main__':
    # 灰度图像
    image = cv2.imread("../tests/hello_world_hand_writen.jpg", cv2.IMREAD_COLOR)
    # 降噪
    denoising = cv2.fastNlMeansDenoising(image)
    bounding_rectangles = get_bounding_rectangles(denoising)
    print(len(bounding_rectangles))

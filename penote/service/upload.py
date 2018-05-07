import logging
import os
import uuid

from werkzeug.utils import secure_filename

from ..config import get_config

LOGGER = logging.getLogger(__name__)
# 被支持的图像文件后缀名
__SUPPORTED_IMAGE_FILE_EXTENSION = {'jpg', 'jpeg', 'bmp'}


def save(file):
    """ 保存上传的文件,以随机UUID保存,并返回文件路径 """
    # 被支持的图像文件后缀名
    extension = __get_support_image_file_extension(file.filename)
    if not extension:
        return None
    else:
        file_key = secure_filename(str(uuid.uuid4()) + '.' + extension)
        file_path = os.path.join(
            get_config().get('source_image_path'),
            file_key
        )
        file.save(file_path)
        file.close()
        LOGGER.info('保存上传文件%s', file_path)
        return file_path


def __get_support_image_file_extension(filename):
    """ 获取被支持的图像文件后缀名 """
    tokens = filename.split('.')
    if len(tokens) < 2:
        return None
    elif tokens[-1].lower() in __SUPPORTED_IMAGE_FILE_EXTENSION:
        return tokens[-1].lower()
    else:
        return None

import logging
import logging.config

import os.path
import yaml


def __check_directories(dir):
    """
    若文件夹dir不存在，则创建，否则不创建
    :param dir: 需要检测的文件夹
    """
    if not os.path.exists(dir):
        os.makedirs(dir)
        LOGGER.info("create directory: %s", dir)


def get():
    """
    加载配置文件
    :return: 配置字典
    """
    global __CONFIG
    # 若__config_json为None，加载文件
    if __CONFIG is None:
        # 配置文件路径
        config_file_path = 'config.yaml'
        # 若配置文件存在
        if os.path.exists(config_file_path):
            # 打开并读取配置文件
            with open(config_file_path, 'rt') as config_file:
                __CONFIG = yaml.safe_load(config_file.read())
                LOGGER.info('Config loaded: %s' % str(__CONFIG))
                __check_directories(__CONFIG['bmp_path'])
                __check_directories(__CONFIG['svg_path'])
                __check_directories(__CONFIG['source_image_path'])
        else:
            # 报错并退出
            LOGGER.error('Config file not found')
            exit(1)
    return __CONFIG


def setup_logging(default_path='logging.yaml', default_level=logging.INFO):
    """
    配置日志
    """
    log_file_directory_path = '../logs'
    # 若日志目录不存在，则创建
    if not os.path.exists(log_file_directory_path):
        os.makedirs(log_file_directory_path)
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


# 配置字典
__CONFIG = None
LOGGER = logging.getLogger(__name__)
# 切换工作路径
path_of_file = os.path.dirname(os.path.abspath(__file__))
os.chdir(path_of_file)
LOGGER.info('Changed the current working directory to %s', path_of_file)

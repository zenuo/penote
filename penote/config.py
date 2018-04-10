import logging
import logging.config

import os.path
import yaml


def get():
    """
    加载配置文件
    :return: 配置字典
    """
    global __config_json
    # 若__config_json为None，加载文件
    if __config_json is None:
        # 配置文件路径
        config_file_path = 'config.yaml'
        # 若配置文件存在
        if os.path.exists(config_file_path):
            # 打开并读取配置文件
            with open(config_file_path, 'rt') as config_file:
                __config_json = yaml.safe_load(config_file.read())
                LOGGER.info('Config loaded: %s' % str(__config_json))
        else:
            # 报错并退出
            LOGGER.error('Config file not found')
            exit(1)
    return __config_json


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
__config_json = None
# 日志
# setup_logging()
LOGGER = logging.getLogger(__name__)
# 切换工作路径
path_of_file = os.path.dirname(os.path.abspath(__file__))
os.chdir(path_of_file)
LOGGER.info('Changed the current working directory to %s', path_of_file)

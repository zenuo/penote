import json
import logging
import os.path

# 配置字典
__config_json = None
# 日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get():
    """
    加载配置文件
    :return: 配置字典
    """
    global __config_json
    # 若__config为None，加载文件
    if __config_json is None:
        # 若配置文件存在
        if os.path.exists('./config.json'):
            # 打开并读取配置文件
            with open('./config.json', 'r') as config_file:
                __config_json = json.load(config_file)
                logger.info('Config loaded: %s' % str(__config_json))
        else:
            # 报错并退出
            print('Config file not found')
            exit(1)
    return __config_json

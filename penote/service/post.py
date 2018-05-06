""" 文章逻辑 """
import logging

from ..config import get_config
from ..data import SESSION_MAKER
from ..models import Post

LOGGER = logging.getLogger(__name__)
CONFIG = get_config()


def get_by_id(id):
    """根据文章ID获取"""
    sess = SESSION_MAKER()
    try:
        return sess.query(Post). \
            filter_by(id=id, is_deleted=0). \
            all()
    except Exception as ex:
        LOGGER.error('根据文章ID获取', ex)
        return None
    finally:
        sess.close()


def get_list_by_user_id(user_id):
    """根据用户ID获取列表"""
    sess = SESSION_MAKER()
    try:
        return sess.query(Post). \
            filter_by(user_id=id, is_deleted=0). \
            all()
    except Exception as ex:
        LOGGER.error('根据用户ID获取列表', ex)
        return []
    finally:
        sess.close()

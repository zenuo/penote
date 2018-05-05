import logging

from ..data import SESSION_MAKER
from ..models import Character

LOGGER = logging.getLogger(__name__)


def get_list_by_para_id(para_id):
    """ 根据段落查询字符列表 """
    sess = SESSION_MAKER()
    try:
        return sess.query(Character). \
            filter_by(paragraph_id=para_id, is_deleted=0). \
            order_by(Character.index_number). \
            all()
    except Exception as ex:
        LOGGER.error('根据段落查询字符列表', ex)
        return []
    finally:
        sess.close()


def get_by_character_id(character_id):
    """根据字符ID获取字符信息"""
    sess = SESSION_MAKER()
    try:
        return sess.query(Character). \
            filter_by(id=character_id, is_deleted=0). \
            first()
    except Exception as ex:
        LOGGER.error('根据字符ID获取字符信息', ex)
        return None
    finally:
        sess.close()

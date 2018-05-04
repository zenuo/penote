import logging

from ..data import SESSION_MAKER
from ..models import Character

LOGGER = logging.getLogger(__name__)


def get(para):
    """ 根据段落查询字符列表 """
    sess = SESSION_MAKER()
    try:
        return sess.query(Character). \
            filter_by(paragraph_id=para, is_deleted=0). \
            order_by(Character.index_number). \
            all()
    except Exception as ex:
        LOGGER.error('查询段落异常', ex)
    finally:
        sess.close()

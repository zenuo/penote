import logging

from ..data import SESSION_MAKER
from ..models import Paragraph

# 日志
LOGGER = logging.getLogger(__name__)


def get_list_by_post_id(post_id):
    """ 根据文章ID获取段落列表 """
    sess = SESSION_MAKER()
    try:
        return sess.query(Paragraph). \
            filter_by(post_id=post_id, is_deleted=0). \
            order_by(Paragraph.created). \
            all()
    except Exception as ex:
        LOGGER.error('根据文章ID获取段落列表', ex)
    finally:
        sess.close()


def get_by_para_id(paragraph_id):
    """根据段落ID获取"""
    sess = SESSION_MAKER()
    try:
        return sess.query(Paragraph). \
            filter_by(id=paragraph_id, is_deleted=0). \
            first()
    except Exception as ex:
        LOGGER.error('根据段落ID获取', ex)
    finally:
        sess.close()

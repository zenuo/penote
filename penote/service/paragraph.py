import logging
from penote.data import SESSION_MAKER
from penote.models import Paragraph

# 日志
LOGGER = logging.getLogger(__name__)


def get(id, user=None, post=None):
    sess = SESSION_MAKER()
    try:
        return sess.query(Paragraph).\
                filter_by(id=id, is_deleted=0).\
                all()
    except Exception as ex:
        LOGGER.error('查询段落异常', ex)
    finally:
        sess.close()

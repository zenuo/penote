""" 文章逻辑 """
import logging
import os
import uuid

from werkzeug.utils import secure_filename

from ..config import get_config
from ..data import SESSION_MAKER
from ..models import Post

LOGGER = logging.getLogger(__name__)
CONFIG = get_config()


def get(id, user=None):
    sess = SESSION_MAKER()
    try:
        return sess.query(Post).\
            filter_by(id=id, is_deleted=0).\
            all()
    except Exception as ex:
        LOGGER.error('查询文章失败', ex)
    finally:
        sess.close()

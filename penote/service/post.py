""" 文章逻辑 """
import datetime
import logging
import uuid

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
            first()
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


def create(json, user_id):
    """创建"""
    sess = SESSION_MAKER()
    try:
        post_id = str(uuid.uuid4())
        new_post = Post(
            id=post_id,
            user_id=user_id,
            title=json.get('title')
        )
        sess.add(new_post)
        sess.commit()
        LOGGER.info('创建文章%s', post_id)
        return new_post
    except Exception as ex:
        LOGGER.error('创建文章%s', post_id, ex)
    finally:
        sess.close()


def delete(post_id):
    """删除文章"""
    sess = SESSION_MAKER()
    try:
        LOGGER.info('删除文章')
        sess.query(Post). \
            filter_by(id=post_id). \
            update({'is_deleted': 1, 'updated': datetime.datetime.now()})
        sess.commit()
        return True
    except Exception as ex:
        LOGGER.error('删除文章', ex)
        return False
    finally:
        sess.close()


def get_all():
    """查询所有"""
    sess = SESSION_MAKER()
    try:
        return sess.query(Post). \
            filter_by(is_deleted=0). \
            order_by(Post.updated.desc()). \
            all()
    except Exception as ex:
        LOGGER.error('查询所有', ex)
        return []
    finally:
        sess.close()


def get_list_by_title(key):
    """根据标题查找"""
    sess = SESSION_MAKER()
    try:
        return sess.query(Post). \
            filter(Post.is_deleted == 0, Post.title.like('%%%s%%' % (key))). \
            order_by(Post.updated.desc()). \
            all()
    except Exception as ex:
        LOGGER.error('根据标题查找', ex)
        return []
    finally:
        sess.close()

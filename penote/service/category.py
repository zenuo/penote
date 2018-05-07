import logging
import uuid

from ..data import SESSION_MAKER
from ..models import Category
from ..service import session

LOGGER = logging.getLogger(__name__)


def get_by_user_id_and_name(user_id, name):
    """根据用户ID和名称查询是否存在"""
    sess = SESSION_MAKER()
    try:
        return sess.query(Category). \
            filter_by(user_id=user_id, name=name, is_deleted=0). \
            limit(1). \
            one()
    except Exception as ex:
        LOGGER.error('根据用户ID和名称查询分类异常', ex)
    finally:
        sess.close()


def create(json):
    """新建分类"""
    if {'session', 'name'} != set(json.keys()):
        return None
    session_id = json['session']
    if not session.is_valid(session_id):
        return None
    name = json['name']
    user_id = session.get_user_id_by_id(session_id)
    category_in_db = get_by_user_id_and_name(user_id, name)
    if category_in_db is not None:
        return category_in_db
    else:
        LOGGER.info('新建分类,用户%s,名称%s', user_id, name)
        category = Category(id=str(uuid.uuid4()), user_id=user_id, name=name)
        # 获取会话
        sess = SESSION_MAKER()
        try:
            sess.add(category)
            sess.commit()
            return category
        except Exception as ex:
            LOGGER.error('创建分类异常', ex)
        finally:
            sess.close()


def get_list_by_session_id(session_id):
    """根据会话ID查询分类"""
    # 检查用户是否登录
    if not session.is_valid(session_id):
        return []
    # 获取用户ID
    user_id = session.get_user_id_by_id(session_id)
    # 获取会话
    sess = SESSION_MAKER()
    try:
        return sess.query(Category). \
            filter_by(user_id=user_id, is_deleted=0). \
            all()
    except Exception as ex:
        LOGGER.error('根据会话ID查询分类', ex)
        return []
    finally:
        sess.close()

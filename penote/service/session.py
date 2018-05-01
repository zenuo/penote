import datetime
import logging
import uuid

from flask_restful import abort
from sqlalchemy import func

from ..data import SESSION_MAKER
from ..models import Session, User
from ..service import user

LOGGER = logging.getLogger(__name__)


def is_valid(id):
    """检查会话是否有效"""
    if id is None:
        return False
    else:
        sess = SESSION_MAKER()
        try:
            return sess.query(func.count(Session.id)). \
                       filter_by(id=id, is_deleted=0). \
                       limit(1). \
                       scalar() != 0
        except Exception as ex:
            LOGGER.error('验证会话异常', ex)
        finally:
            sess.close()


def exists_by_user_name(user_name):
    """根据用户名查询是否存在会话"""
    sess = SESSION_MAKER()
    try:
        count = sess.query(func.count(Session.id)). \
            join(User). \
            filter(User.name == user_name, User.is_deleted == 0, Session.is_deleted == 0). \
            limit(1). \
            scalar()
        return count != 0
    except Exception as ex:
        LOGGER.error('根据用户姓名查询会话异常', ex)
    finally:
        sess.close()


def invalidate_by_user_name(user_name):
    """根据用户名删除会话"""
    sess = SESSION_MAKER()
    try:
        user_id = sess.query(User.id). \
            filter_by(name=user_name). \
            limit(1). \
            scalar()
        sess.query(Session). \
            filter_by(user_id=user_id, is_deleted=0). \
            update({'is_deleted': 1, 'updated': datetime.datetime.now()})
        sess.commit()
        LOGGER.info('用户"%s"登出', user_name)
    except Exception as ex:
        LOGGER.error('使无效会话异常', ex)
    finally:
        sess.close()


def login(json):
    """登入"""
    if {'user_name', 'password'} != set(json.keys()):
        abort(400, error='信息不正确')
    user_name = json['user_name']
    password = json['password']
    # 删除原有效会话
    invalidate_by_user_name(user_name)
    sess = SESSION_MAKER()
    try:
        if user.check_password(user_name, password):
            user_id = user.get_id_by_name(user_name)
            s_id = str(uuid.uuid4())
            s = Session(id=s_id, user_id=user_id)
            sess.add(s)
            sess.commit()
            LOGGER.info('用户"%s"登入"%s"', user_name, s_id)
            return {'user_id': user_id, 'session': s_id}
    except Exception as ex:
        LOGGER.error('登入异常', ex)
    finally:
        sess.close()


def logout(id):
    """登出"""
    sess = SESSION_MAKER()
    try:
        ret = sess.query(Session). \
                  filter_by(id=id, is_deleted=0). \
                  update({'is_deleted': 1, 'updated': datetime.datetime.now()}) == 1
        sess.commit()
        return ret
    except Exception as ex:
        LOGGER.error('登出异常', ex)
    finally:
        sess.close()


def get_user_id_by_id(session_id):
    """根据会话ID查询用户ID"""
    sess = SESSION_MAKER()
    try:
        return sess.query(Session.user_id). \
            filter_by(id=session_id, is_deleted=0). \
            limit(1). \
            scalar()
    except Exception as ex:
        LOGGER.error('根据会话ID查询用户ID异常', ex)
    finally:
        sess.close()
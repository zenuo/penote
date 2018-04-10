import datetime
import logging

from flask_restful import abort
from sqlalchemy import func

from ..data import SESSION_MAKER
from ..models import Session, User

LOGGER = logging.getLogger(__name__)


def is_valid(id):
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
    sess = SESSION_MAKER()
    try:
        user_id = sess.query(User.id). \
            filter_by(name=user_name). \
            limit(1). \
            scalar()
        sess.query(Session). \
            filter(Session.user_id == user_id, Session.is_deleted == 0). \
            update({'is_deleted': 1, 'updated': datetime.datetime.now()})
        sess.commit()
    except Exception as ex:
        LOGGER.error('使无效会话异常', ex)
    finally:
        sess.close()


def login(json):
    if {'user_name', 'password'} != set(json.keys()):
        abort(400, error='信息不完整')
    user_name = json['user_name']
    password = json['password']
    if exists_by_user_name(user_name):
        pass
    else:
        sess = SESSION_MAKER()
        try:
            pass
        except Exception as ex:
            LOGGER.error('登入异常', ex)
        finally:
            sess.close()

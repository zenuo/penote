import logging
import uuid
from hashlib import sha3_512

from flask_restful import abort
from sqlalchemy import func

from ..data import SESSION_MAKER
from ..models import User
from ..service import session

# 日志
LOGGER = logging.getLogger(__name__)


def create(json):
    if {'name', 'email', 'bio', 'password'} != set(json.keys()):
        abort(400, error='信息不完全')
    exists_same_name = get_id_by_name(json['name']) is not None
    if exists_same_name:
        abort(400, error='存在同名用户')
    else:
        sess = SESSION_MAKER()
        try:
            user = User(
                id=str(uuid.uuid4()),
                name=json['name'],
                email=json['email'],
                bio=json['bio'],
                password_hash=sha3_512(json['password'].encode('utf-8')).hexdigest()
            )
            sess.add(user)
            sess.commit()
            return user, 201
        except Exception as ex:
            LOGGER.error('异常', ex)
            raise ex
        finally:
            sess.close()


def get_id_by_name(name):
    sess = SESSION_MAKER()
    try:
        return sess.query(User.id).filter_by(name=name, is_deleted=0).limit(1).scalar()
    except Exception as ex:
        LOGGER.error('查询是否存在指定用户名用户异常', ex)
        raise ex
    finally:
        sess.close()


def exists_by_id(id, is_deleted):
    sess = SESSION_MAKER()
    try:
        return sess.query(func.count(User.id)).filter_by(id=id, is_deleted=is_deleted).limit(1).scalar() != 0
    except Exception as ex:
        LOGGER.error('查询是否存在指定ID用户异常', ex)
        raise ex
    finally:
        sess.close()


def invalidate(id, session_id):
    """删除（禁用）用户"""
    if not session.is_valid(session_id):
        abort(403, error='无权限，请登录')
    if exists_by_id(id, 0):
        sess = SESSION_MAKER()
        try:
            sess.query(User).filter_by(id=id, is_deleted=0).update({'is_deleted': 1})
            sess.commit()
        except Exception as ex:
            LOGGER.error('禁用用户异常', ex)
            raise ex
        finally:
            sess.close()
    else:
        abort(404, error='不存在指定用户')


def validate(id, session):
    if not session.is_valid(session):
        abort(403, error='无权限，请登录')
    if exists_by_id(id, 1):
        sess = SESSION_MAKER()
        try:
            sess.query(User).filter_by(id=id, is_deleted=1).update({'is_deleted': 0})
            sess.commit()
        except Exception as ex:
            LOGGER.error('禁用用户异常', ex)
            raise ex
        finally:
            sess.close()
    else:
        abort(404, error='不存在指定的被禁用的用户')


def check_password(user_name, password):
    sess = SESSION_MAKER()
    try:
        user_id = sess.query(User.id). \
            filter_by(name=user_name, password_hash=sha3_512(password.encode('utf-8')).hexdigest(), is_deleted=0). \
            limit(1). \
            scalar()
        if user_id:
            return True, user_id
        else:
            return False, None
    except Exception as ex:
        LOGGER.error('检查密码异常', ex)
    finally:
        sess.close()

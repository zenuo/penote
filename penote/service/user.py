import logging
import uuid
from hashlib import sha3_512

from flask_restful import abort

from ..data import SESSION_MAKER
from ..models import User

# 日志
LOGGER = logging.getLogger(__name__)


def create(json):
    if {'name', 'email', 'bio', 'password'} != set(json.keys()):
        abort(400, error='信息不完全')
    exists_same_name = exists_name(json['name'])
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


def exists_name(name):
    sess = SESSION_MAKER()
    try:
        return sess.query(User).filter(User.name == name).count() != 0
    except Exception as ex:
        LOGGER.error("查询同名用户异常", ex)
        raise ex
    finally:
        sess.close()

import logging
import os
from werkzeug.utils import secure_filename

from penote import config
from penote.data import SESSION_MAKER
from penote.models import Post

LOGGER = logging.getLogger(__name__)
CONFIG = config.get()


def upload(file):
    file_path = os.path.join(CONFIG['source_image_path'], secure_filename(file.filename))
    file.save(file_path)
    LOGGER.info('保存上传文件%s' % file_path)
    return 'true'


def get(id, user=None):
    sess = SESSION_MAKER()
    try:
        return sess.query(Post).filter_by(id=id, is_deleted=0).all()
    except Exception as ex:
        LOGGER.error('查询文章失败', ex)
    finally:
        sess.close()

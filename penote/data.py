import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from penote.entity import BASE

LOGGER = logging.getLogger(__name__)
__ENGINE = create_engine('sqlite:///penote.db', echo=True)
# 若不存在表，则创建表
BASE.metadata.create_all(__ENGINE)
SESSION_MAKER = sessionmaker(bind=__ENGINE)
# 会话
SESSION = SESSION_MAKER()

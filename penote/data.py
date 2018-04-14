import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import BASE as __BASE

# LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.INFO)
__ENGINE = create_engine('sqlite:///penote.db', echo=True)
# 若不存在表，则创建表
__BASE.metadata.create_all(__ENGINE)
SESSION_MAKER = sessionmaker(bind=__ENGINE, expire_on_commit=False)

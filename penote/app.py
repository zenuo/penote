""" 主模块 """
import logging
import os

from flask import Flask, request
from flask_restful import Api

from .resources import (Categories, CharacterList, Characters, Paragraphs,
                        Posts, Sessions, Users, PostList, ParagraphList)
from .service import upload, session
from .utils import photo2svg

# 日志
LOGGER = logging.getLogger(__name__)
# Flask应用实例
__APP = Flask(__name__)


@__APP.route('/api/', methods=['GET'])
def hello():
    """ 欢迎页面 """
    return 'Welcome to Penote API! https://github.com/zenuo/penote.git\r\n'


@__APP.route('/api/uploads', methods=['POST'])
def upload_file():
    """ 上传文件, 返回由文件创建的段落ID """
    if request.method == 'POST':
        # 会话ID
        session_id = request.headers.get('session')
        if session.is_valid(session_id):
            # 文件实例
            file = request.files.get('file')
            # 文章ID
            post_id = request.headers.get('post')
            # 段落照片源文件
            paragraph_file_path = upload.save(file)
            return photo2svg(paragraph_file_path, post_id)
    return ''


if __name__ == '__main__':
    """ 主方法 """
    # 记录进程号
    LOGGER.info('PID=%d', os.getpid())
    # 资源类映射
    __API = Api(__APP, prefix='/api')
    __API.add_resource(Users, '/users', '/users/<string:user_id>')
    __API.add_resource(Posts, '/posts', '/posts/<string:post_id>')
    __API.add_resource(PostList, '/post-list')
    __API.add_resource(Paragraphs, '/paragraphs', '/paragraphs/<string:paragraph_id>')
    __API.add_resource(ParagraphList, '/paragraph-list')
    __API.add_resource(Characters, '/characters', '/characters/<string:character_id>')
    __API.add_resource(CharacterList, '/character-list')
    __API.add_resource(Categories, '/categories')
    __API.add_resource(Sessions, '/sessions', '/sessions/<string:session_id>')
    # 启动flask实例
    __APP.run(debug=False, port=5000)

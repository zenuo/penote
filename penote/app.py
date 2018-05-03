""" 启动模块 """
import logging
import json

from flask import Flask, request
from flask_restful import Api

from .resources import (Categories, Characters, Paragraphs, Posts, Sessions,
                        Users)
from .service import post, upload

# 日志
LOGGER = logging.getLogger(__name__)
# Flask应用实例
__APP = Flask(__name__)
__API = Api(__APP, prefix='/api')


@__APP.route('/api/', methods=['GET'])
def hello():
    """ 欢迎页面 """
    return 'Welcome to Penote API! https://github.com/zenuo/penote.git\r\n'


@__APP.route('/api/uploads', methods=['POST'])
def upload_file():
    """ 文件上传 """
    if request.method == 'POST':
        file = request.files['file']
        return upload.save(file)
    else:
        return json.dumps({'key': None})

__API.add_resource(Users, '/users')
__API.add_resource(Posts, '/posts')
__API.add_resource(Paragraphs, '/paragraphs')
__API.add_resource(Characters, '/characters')
__API.add_resource(Categories, '/categories')
__API.add_resource(Sessions, '/sessions', '/sessions/<string:session_id>')


if __name__ == '__main__':
    """ 主方法 """
    __APP.run(debug=False, port=5000)

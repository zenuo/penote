""" 启动模块 """
import logging

from flask import Flask, request
from flask_restful import Api, Resource, marshal_with, fields, reqparse

from .service import user, post, paragraph, character, session, category

# 日志
LOGGER = logging.getLogger(__name__)
# Flask应用实例
__APP = Flask(__name__)
__API = Api(__APP, prefix='/api')
# 解析器
PARSER = reqparse.RequestParser()
PARSER.add_argument('id', type=str)
PARSER.add_argument('session', type=str)
PARSER.add_argument('title', type=str)
PARSER.add_argument('user', type=str)
PARSER.add_argument('para', type=str)
PARSER.add_argument('post', type=str)


@__APP.route('/api/', methods=['GET'])
def hello():
    """ 欢迎页面 """
    return 'Welcome to Penote API! https://github.com/zenuo/penote.git\r\n'


@__APP.route('/api/uploads', methods=['POST'])
def upload_file():
    """ 文件上传 """
    if request.method == 'POST':
        file = request.files['file']
        return post.upload(file)
    else:
        return 'false'


class Users(Resource):
    user_fields = {
        'id': fields.String,
        'name': fields.String,
        'email': fields.String,
        'bio': fields.String,
        'updated': fields.DateTime(dt_format='iso8601')
    }

    @marshal_with(user_fields)
    def post(self):
        json = request.get_json(force=True)
        return user.create(json)

    def delete(self):
        args = PARSER.parse_args()
        id = args['id']
        session = args['session']
        return user.invalidate(id, session)


class Posts(Resource):
    post_fields = {'id': fields.String,
                   'user_id': fields.String,
                   'title': fields.String,
                   'updated': fields.DateTime(dt_format='iso8601')}

    @marshal_with(post_fields)
    def get(self):
        args = PARSER.parse_args()
        id = args['id']
        user = args['user']
        return post.get(id, user=user)


class Paragraphs(Resource):
    paragraph_fields = {
        'id': fields.String,
        'post_id': fields.String,
        'index_number': fields.Integer,
        'updated': fields.DateTime(dt_format='iso8601')
    }

    @marshal_with(paragraph_fields)
    def get(self):
        args = PARSER.parse_args()
        # 段落ID
        id = args['id']
        # 文章ID
        post = args['post']
        return paragraph.get(id, post=post)


class Characters(Resource):
    character_fields = {
        'id': fields.String,
        'index_number': fields.Integer,
        'updated': fields.DateTime(dt_format='iso8601')}

    @marshal_with(character_fields)
    def get(self):
        args = PARSER.parse_args()
        # 段落ID
        para = args['para']
        return character.get(para)


class Sessions(Resource):
    def post(self):
        json = request.get_json(force=True)
        return session.login(json)

    def delete(self):
        args = PARSER.parse_args()
        id = args['id']
        return session.logout(id)


class Categories(Resource):
    category_fileds = {
        'id': fields.String,
        'name': fields.String
    }

    @marshal_with(category_fileds)
    def get(self):
        args = PARSER.parse_args()
        session_id = args['session']
        return category.get(session_id)

    @marshal_with(category_fileds)
    def post(self):
        json = request.get_json(force=True)
        return category.create(json)


__API.add_resource(Users, '/users')
__API.add_resource(Posts, '/posts')
__API.add_resource(Paragraphs, '/paragraphs')
__API.add_resource(Characters, '/characters')
__API.add_resource(Categories, '/categories')
__API.add_resource(Sessions, '/sessions')


def run():
    __APP.run(debug=False)

""" 资源模块 """
from flask import request
from flask_restful import Resource, fields, marshal_with

from .service import category, character, paragraph, post, session, user


class Users(Resource):
    """ 用户资源类 """
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


class Posts(Resource):
    """ 文章资源类 """
    post_fields = {'id': fields.String,
                   'user_id': fields.String,
                   'title': fields.String,
                   'updated': fields.DateTime(dt_format='iso8601')}

    @marshal_with(post_fields)
    def get(self):
        post_id = request.args.get('id')
        user = request.args.get('user')
        return post.get(post_id, user=user)


class Paragraphs(Resource):
    """ 段落资源类 """
    paragraph_fields = {
        'id': fields.String,
        'post_id': fields.String,
        'index_number': fields.Integer,
        'updated': fields.DateTime(dt_format='iso8601')
    }

    @marshal_with(paragraph_fields)
    def get(self):
        # 段落ID
        paragraph_id = request.args.get('id')
        # 文章ID
        post_id = request.args.get('post')
        return paragraph.get(paragraph_id, post=post_id)


class Characters(Resource):
    """ 字符资源类 """
    character_fields = {
        'id': fields.String,
        'index_number': fields.Integer,
        'updated': fields.DateTime(dt_format='iso8601')}

    @marshal_with(character_fields)
    def get(self):
        # 段落ID
        paragraph_id = request.args.get('para')
        return character.get(paragraph_id)


class Sessions(Resource):
    """ 会话资源类 """

    def post(self):
        json = request.get_json(force=True)
        return session.signin(json)

    def delete(self, session_id):
        return session.signout(session_id)


class Categories(Resource):
    """ 分类资源类 """
    category_fileds = {
        'id': fields.String,
        'name': fields.String
    }

    @marshal_with(category_fileds)
    def get(self):
        session_id = request.headers.get('session')
        return category.get(session_id)

    @marshal_with(category_fileds)
    def post(self):
        json = request.get_json(force=True)
        return category.create(json)

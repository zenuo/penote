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

    @marshal_with(user_fields)
    def get(self, user_id):
        session_id = request.headers.get('session')
        if session.is_valid(session_id):
            return user.get_by_user_id(user_id)
        else:
            return None


class Posts(Resource):
    """ 文章资源类 """
    post_fields = {'id': fields.String,
                   'user_id': fields.String,
                   'title': fields.String,
                   'created': fields.DateTime(dt_format='iso8601'),
                   'updated': fields.DateTime(dt_format='iso8601')}

    @marshal_with(post_fields)
    def get(self):
        session_id = request.headers.get('session')
        if session.is_valid(session_id):
            post_id = request.args.get('id')
            return post.get_by_id(post_id)
        else:
            return None


class PostList(Resource):
    @marshal_with(Posts.post_fields)
    def get(self):
        session_id = request.headers.get('session')
        if session.is_valid(session_id):
            user_id = request.args.get('user')
            return post.get_list_by_user_id(user_id)
        else:
            return []


class Paragraphs(Resource):
    """ 段落资源类 """
    paragraph_fields = {
        'id': fields.String,
        'post_id': fields.String,
        'index_number': fields.Integer,
        'created': fields.DateTime(dt_format='iso8601'),
        'updated': fields.DateTime(dt_format='iso8601')
    }

    @marshal_with(paragraph_fields)
    def get(self, paragraph_id):
        session_id = request.headers.get('session')
        if session.is_valid(session_id):
            return paragraph.get_by_para_id(paragraph_id)
        else:
            return None

    def post(self):
        pass


class ParagraphList(Resource):
    @marshal_with(Paragraphs.paragraph_fields)
    def get(self):
        # 段落ID
        paragraph_id = request.args.get('id')
        # 文章ID
        post_id = request.args.get('post')
        return paragraph.get_list_by_post_id(paragraph_id)


class Characters(Resource):
    """ 字符资源类 """
    character_fields = {
        'id': fields.String,
        'index_number': fields.Integer,
        'paragraph_id': fields.String,
        'created': fields.DateTime(dt_format='iso8601'),
        'updated': fields.DateTime(dt_format='iso8601')}

    @marshal_with(character_fields)
    def get(self, character_id):
        session_id = request.headers.get('session')
        if session.is_valid(session_id):
            return character.get_by_character_id(character_id)
        else:
            return None


class CharacterList(Resource):
    """ 字符列表 """

    @marshal_with(Characters.character_fields)
    def get(self):
        """ 由段落ID查询字符列表 """
        session_id = request.headers.get('session')
        if session.is_valid(session_id):
            paragraph_id = request.args.get('para')
            return character.get_list_by_para_id(paragraph_id)
        else:
            return []


class Sessions(Resource):
    """ 会话资源类 """

    def post(self):
        """ 登入 """
        json = request.get_json(force=True)
        return session.sign_in(json.get('user_name'), json.get('password'))

    def delete(self, session_id):
        """ 登出 """
        if session.is_valid(session_id):
            return session.signout(session_id)
        else:
            return False


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

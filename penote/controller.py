from flask import Flask, request
from flask_restful import Api, Resource, marshal_with, fields

from penote.service import user


class Welcome(Resource):
    def get(self):
        return 'Welcome to penote api, :-)'


class Users(Resource):
    user_fields = {
        'id': fields.String,
        'name': fields.String,
        'email': fields.String,
        'bio': fields.String,
        'created': fields.DateTime(dt_format='iso8601'),
        'updated': fields.DateTime(dt_format='iso8601')
    }

    @marshal_with(user_fields)
    def post(self):
        json = request.get_json(force=True)
        return user.create(json)


__APP = Flask(__name__)
__API = Api(__APP, default_mediatype='application/json; charset=utf-8')
__API.add_resource(Welcome, '/')
__API.add_resource(Users, '/users')

if __name__ == '__main__':
    __APP.run(debug=False)

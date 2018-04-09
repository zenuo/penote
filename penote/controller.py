from flask import Flask
from flask_restful import Api, Resource, marshal_with, fields

from penote.entity import Rectangle

app = Flask(__name__)
api = Api(app)

rectangle_fields = {
    'x': fields.Integer,
    'y': fields.Integer,
    'w': fields.Integer,
    'h': fields.Integer
}


class Rectangles(Resource):
    @marshal_with(rectangle_fields)
    def get(self):
        return Rectangle(1, 2, 3, 4)


# class Posts(Resource):
#     @marshal_with()
api.add_resource(Rectangles, '/')

if __name__ == '__main__':
    app.run(debug=False)

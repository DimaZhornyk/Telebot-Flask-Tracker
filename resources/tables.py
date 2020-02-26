from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from database import db


class Tables(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Name', type=str, required=True, help='Name cannot be left blank')
        data = parser.parse_args()
        array = list(db[data['Name']].find())
        for el in array:
            del el['_id']
        return array

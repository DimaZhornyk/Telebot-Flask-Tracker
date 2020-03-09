from flask_jwt_extended import create_access_token
from flask_restful import reqparse, Resource

from database import Users

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help='This field cannot be left blank')
_user_parser.add_argument('password', type=str, required=True, help='This field cannot be left blank')


class UserLogin(Resource):

    @classmethod
    def post(cls):
        # gets data,checks user and creates access token and refresh token, return them
        data = _user_parser.parse_args()

        user_password = Users.find_one({"username": data['username']})['password']
        if user_password and user_password == data['password']:
            access_token = create_access_token(identity=data['username'])
            return {'access_token': access_token, 'expiration_time': 7200}, 200

        return {'message': 'Password is incorrect'}, 401

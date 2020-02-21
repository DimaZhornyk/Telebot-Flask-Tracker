from flask_jwt_extended import create_refresh_token, create_access_token, jwt_refresh_token_required, get_jwt_identity
from flask_restful import reqparse, Resource
from sqlalchemy import select

from connection import engine, Users

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help='This field cannot be left blank')
_user_parser.add_argument('password', type=str, required=True, help='This field cannot be left blank')


class UserLogin(Resource):

    @classmethod
    def post(cls):
        # gets data,checks user and creates access token and refresh token, return them
        conn = engine.connect()
        data = _user_parser.parse_args()

        user_password = \
            conn.execute(select([Users.c.password]).where(Users.c.username == data['username'])).fetchall()[0][0]
        user_id = \
            conn.execute(select([Users.c.id]).where(Users.c.username == data['username'])).fetchall()[0][0]

        if user_password and user_password == data['password']:
            access_token = create_access_token(identity=user_id, fresh=True)
            return {'access_token': access_token}, 200

        return {'message': 'Password is incorrect'}, 401

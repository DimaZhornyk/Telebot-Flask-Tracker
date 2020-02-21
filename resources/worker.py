from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import select

from connection import engine, Global


class Worker(Resource):
    @jwt_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be left blank')
        parser.add_argument('surname', type=str, required=True, help='Name cannot be left blank')
        data = parser.parse_args()
        conn = engine.connect()
        if conn.execute(select([Global.c.id]).where(Global.c.surname == data['surname']).where()).fetchall():
            try:
                conn.execute(
                    Global.delete().where(Global.c.name == data['name']).where(Global.c.surname == data['surname']))
            except:
                return {'message': 'Error occurred deleting the user'}, 500
        else:
            return {'message': "User doesn't exist"}
        return {'message': 'Worker successfully deleted'}

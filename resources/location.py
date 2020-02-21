from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import select

from connection import engine, Locations


class Location(Resource):
    @jwt_required
    def post(self):
        conn = engine.connect()
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be left blank')
        parser.add_argument('lat', type=float, required=True, help='Latitude cannot be left blank')
        parser.add_argument('lng', type=float, required=True, help='Longitude cannot be left blank')
        data = parser.parse_args()

        if conn.execute(select([Locations.c.id]).where(Locations.c.name == data['name'])).fetchall():
            return {'message': 'Location with this name already exists'}, 400
        else:
            conn.execute(Locations.insert().values(name=data['name'], lat=data['lat'], lng=data['lng']))
        return {'message': 'Location added successfully'}

    @jwt_required
    def delete(self):
        conn = engine.connect()
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be left blank')
        data = parser.parse_args()
        try:
            conn.execute(Locations.delete().where(Locations.c.name == data['name']))
        except:
            return {'message': 'An error occurred during deleting'}, 400
        return {'message': 'Location deleted successfully'}, 200

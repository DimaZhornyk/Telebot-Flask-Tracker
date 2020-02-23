from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import select
from connection import engine, History, Global, Locations


class WorkerHistory(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='Id cannot be left blank')
        data = parser.parse_args()
        conn = engine.connect()
        out = conn.execute(select([History]).where(History.c.user_id == data['id'])).fetchall()
        return {'message': [dict(row) for row in out]}


class Home(Resource):
    @jwt_required
    def get(self):
        conn = engine.connect()
        data = conn.execute(select(
            [Global.c.id, Global.c.name, Global.c.surname, Global.c.total_hours, Global.c.total_minutes,
             Global.c.last_project, Global.c.last_job])).fetchall()
        return {'message': [dict(row) for row in data]}


class LocationsView(Resource):
    @jwt_required
    def post(self):
        conn = engine.connect()
        data = conn.execute(select([Locations.c.id, Locations.c.name, Locations.c.lat, Locations.c.lng])).fetchall()
        return {'message': [dict(row) for row in data]}

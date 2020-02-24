from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import select
from connection import engine, Global


class Update(Resource):
    @jwt_required
    def post(self):
        conn = engine.connect()
        parser = reqparse.RequestParser()
        parser.add_argument('toDelete', type=str)
        parser.add_argument('toUpdate', type=str)
        data = parser.parse_args()
        try:
            ids = [int(i) for i in data['toDelete'].split(',')]
            for worker_id in ids:
                if conn.execute(select([Global.c.id]).where(Global.c.id == worker_id)):
                    conn.execute(Global.delete().where(Global.c.id == worker_id))
        except:
            pass
        try:
            for worker in eval(data['toUpdate']):
                key = list(worker.items())[0][0]
                arg = list(worker.items())[0][1]
                if key == 'id':
                    _id = int(arg)
                if key == 'name':
                    _name = arg
                if key == 'surname':
                    _surname = arg
                if key == 'total_hours':
                    _total_hours = int(arg)
                if key == 'total_minutes':
                    _total_minutes = int(arg)
                if key == 'total_seconds':
                    _total_seconds = int(arg)
                if key == 'last_project':
                    _last_project = arg
                if key == 'last_job':
                    _last_job = arg
                if key == 'lastLat':
                    _last_lat = float(arg)
                if key == 'lastLng':
                    _last_lng = float(arg)
            if conn.execute(select([Global.c.id]).where(Global.c.id == _id)):
                conn.execute(
                    Global.update().values(name=_name, surname=_surname, total_hours=_total_hours,
                                           total_minutes=_total_minutes, total_seconds=_total_seconds,
                                           last_project=_last_project, last_job=_last_job, lastLat=_last_lat,
                                           lastLng=_last_lng, project_chosen=_last_project).where(
                        Global.c.id == _id))
        except Exception as e:
            return {'exception': e}
        return {'message': "Successfully updated"}

from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from database import History, Global, Locations


class WorkerHistory(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Telegram', type=int, required=True, help='Id cannot be left blank')
        data = parser.parse_args()
        out = []
        for obj in History.find({"user_id": data['Telegram']}):
            to_return = {"Telegram": obj["user_id"], "Name": obj["name"], "Surname": obj["surname"],
                         "Time written": obj['time_written'],
                         "Time": obj["time"],
                         "Project": obj["project"], "Work": obj["work"]}
            out.append(to_return)
        return {'message': out}


class Home(Resource):
    @jwt_required
    def get(self):
        try:
            context = []
            for obj in Global.find():
                data = {"Telegram": obj["tg_id"], "Name": obj["name"], "Surname": obj["surname"],
                        "Total time": obj["total_time"],
                        "Last project": Locations.find_one({"_id": obj["last_project"]})['name'],
                        "Last job": obj["last_job"]}
                context.append(data)
            return {"message": context}
        except:
            return {"message": "Exception occurred"}


class LocationsView(Resource):
    @jwt_required
    def post(self):
        ans = []
        for obj in Locations.find():
            to_return = {"Name": obj["name"], "Latitude": obj["lat"], "Longitude": obj["lng"]}
            ans.append(to_return)
        return {'message': ans}

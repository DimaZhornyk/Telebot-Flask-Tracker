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
                         "Hours": obj["hours"], "Minutes": obj["minutes"],
                         "Time": obj["time"],
                         "Project": obj["project"], "Work": obj["work"]}
            out.append(to_return)
        return {'message': out}


class LocationsView(Resource):
    @jwt_required
    def post(self):
        ans = []
        for obj in Locations.find():
            to_return = {"Name": obj["name"], "Latitude": obj["lat"], "Longitude": obj["lng"]}
            ans.append(to_return)
        return {'message': ans}

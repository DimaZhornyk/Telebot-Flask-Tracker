from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from database import Global


class Update(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('toDelete', type=str)
        parser.add_argument('toUpdate', type=str)
        data = parser.parse_args()
        try:
            ids = [int(i) for i in data['toDelete'].split(',')]
            for worker_id in ids:
                if Global.find_one({"tg_id": worker_id}):
                    Global.delete_one({"tg_id": worker_id})
        except:
            pass
        try:
            for obj in eval(data['toUpdate']):
                Global.update_one({"tg_id": obj["Telegram"]},
                                  {"$set": {"name": obj['Name'],
                                            "surname": obj["Surname"], "total_time": obj["Total time"],
                                            "last_project": obj["Last project"], "last_job": obj["Last job"]}})

        except:
            return {"message": "An error occurred when updating a user"}
        return {'message': "Successfully updated"}

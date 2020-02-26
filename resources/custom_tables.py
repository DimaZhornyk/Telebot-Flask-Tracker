from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from database import CustomTables, Global, Locations


class CreateCustomTable(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True, help='Name cannot be left blank')
        parser.add_argument("workers", type=str)
        data = parser.parse_args()
        if CustomTables.find_one({"name": data['name']}):
            return {"message": "Table with this name already exists"}
        CustomTables.insert_one(data)
        return {"message": "Table successfully created"}


class ReturnCustomTable(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True, help='Name cannot be left blank')
        data = parser.parse_args()
        table = CustomTables.find_one({"name": data['name']})
        if table:
            workers = eval(table['workers'])
            out = []
            for worker_tg in workers:
                obj = Global.find_one({"tg_id": worker_tg})
                if obj:
                    to_return = {"Telegram": obj["tg_id"], "Name": obj["name"], "Surname": obj["surname"],
                                 "Total time": obj["total_time"],
                                 "Last project": Locations.find_one({"_id": obj["last_project"]})['name'],
                                 "Last job": obj["last_job"], "Last latitude": obj['last_lat'],
                                 "Last longitude": obj['last_lng']}
                    out.append(to_return)
            return {"name": data['name'], "workers": out}
        return {"message": "This table doesnt exist"}

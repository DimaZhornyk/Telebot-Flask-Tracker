from database import db
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class TableNames(Resource):
    @jwt_required
    def post(self):
        all_names = db.list_collection_names()
        all_names.remove('sequences')
        all_names.remove('Metadata')
        all_names.remove('Users')
        return all_names


class RequiredFields(Resource):
    @jwt_required
    def post(self):
        return db["Metadata"].find_one({"Name": 'Required fields'})["keys"]

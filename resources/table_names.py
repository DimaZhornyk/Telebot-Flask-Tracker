from database import db
from flask_jwt_extended import jwt_required
from flask_restful import Resource

class TableNames(Resource):
    @jwt_required
    def post(self):
        return db.list_collection_names()
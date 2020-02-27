from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from database import db


class Tables(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be left blank')
        data = parser.parse_args()
        array = list(db[data['name']].find())
        for el in array:
            del el['_id']
        return array

    @jwt_required
    def patch(self):
        data = request.get_json(force=True)
        print(data)
        table_name = data['tableName']

        if 'rowsToEdit' in data:
            rowsToEdit = data['rowsToEdit']
            for el in rowsToEdit:
                query = {'ID': el['ID']}
                new_values = {'$set': el}
                db[table_name].update_one(query, new_values)

        if 'rowsToDelete' in data:
            rowsToDelete = eval(data['rowsToDelete'])
            for index in rowsToDelete:
                query = {'ID', index}
                db[table_name].delete_one(query)

        if 'rowsToAdd' in data:
            rowsToAdd = data['rowsToAdd']
            print(type(rowsToAdd))
            db[table_name].insert_many(rowsToAdd)





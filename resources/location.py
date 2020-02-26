from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from database import Locations


class Location(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Name', type=str, required=True, help='Name cannot be left blank')
        parser.add_argument('Latitude', type=float, required=True, help='Latitude cannot be left blank')
        parser.add_argument('Longitude', type=float, required=True, help='Longitude cannot be left blank')
        data = parser.parse_args()

        if Locations.find_one({"name": data['Name']}):
            return {'message': 'Location with this name already exists'}, 400
        else:
            Locations.insert_one({"name": data["Name"], "lat": data["Latitude"], "lng": data["Longitude"]})
        return {'message': 'Location added successfully'}

    @jwt_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Name', type=str, required=True, help='Name cannot be left blank')
        data = parser.parse_args()
        try:
            Locations.delete_one({"name": data["Name"]})
        except:
            return {'message': 'An error occurred during deleting'}, 400
        return {'message': 'Location deleted successfully'}, 200

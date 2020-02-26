from flask_restful import Resource, reqparse
from database import CustomTables


class CreateCustomTable(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("Data", type=str, required=True, help='Data cannot be left blank')
        data = parser.parse_args()
        print(eval(data))


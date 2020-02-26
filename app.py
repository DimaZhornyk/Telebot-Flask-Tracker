from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask import Flask, redirect, render_template

from database import Global, Locations
from resources.custom_tables import CreateCustomTable, ReturnCustomTable
from resources.location import Location
from resources.update import Update
from resources.user import UserLogin
from resources.gets import WorkerHistory, LocationsView
from flask_cors import CORS

app = Flask(__name__,
            static_url_path='',
            static_folder="C:\js_project\my-first-svelte-project\public",
            )
api = Api(app)
CORS(app)
app.secret_key = 'sssss'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWTManager(app)


@app.route('/', methods=['GET'])
def home():
    try:
        context = []
        for obj in Global.find():
            data = {"Telegram": obj["tg_id"], "Name": obj["name"], "Surname": obj["surname"],
                    "Total hours": obj["total_hours"],
                    "Total minutes": obj["total_minutes"], "Total seconds": obj["total_seconds"],
                    "Last project": Locations.find_one({"_id": obj["last_project"]})['name'],
                    "Last job": obj["last_job"]}
            context.append(data)
        return {"message": context}
    except:
        return {"message": "Exception occurred"}


api.add_resource(LocationsView, '/locations/')
api.add_resource(Location, '/location/')
api.add_resource(UserLogin, '/login/')
api.add_resource(WorkerHistory, '/history/')
api.add_resource(Update, '/update/')
api.add_resource(CreateCustomTable, '/createCustomTable/')
api.add_resource(ReturnCustomTable, '/customTable/')


@app.route('/<path:page>')
def allGets(page):
    return redirect('/')


if __name__ == '__main__':
    app.run()

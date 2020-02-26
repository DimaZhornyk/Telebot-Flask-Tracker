from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask import Flask, redirect, render_template

from resources.custom_tables import CreateCustomTable
from resources.location import Location
from resources.update import Update
from resources.user import UserLogin
from resources.gets import WorkerHistory, LocationsView
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)
app.secret_key = 'sssss'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWTManager(app)


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


api.add_resource(LocationsView, '/locations/')
api.add_resource(Location, '/location/')
api.add_resource(UserLogin, '/login/')
api.add_resource(WorkerHistory, '/history/')
api.add_resource(Update, '/update/')
api.add_resource(CreateCustomTable, '/createCustomTable/')


@app.route('/<path:page>')
def allGets(page):
    return redirect('/')


if __name__ == '__main__':
    app.run()

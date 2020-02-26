from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask import Flask, redirect

from resources.location import Location
from resources.update import Update
from resources.user import UserLogin
from resources.gets import WorkerHistory, LocationsView, Home

app = Flask(__name__)
api = Api(app)
app.secret_key = 'sssss'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWTManager(app)

api.add_resource(Home, '/')
api.add_resource(LocationsView, '/locations/')
api.add_resource(Location, '/location/')
api.add_resource(UserLogin, '/login/')
api.add_resource(WorkerHistory, '/history/')
api.add_resource(Update, '/update/')


@app.route('/<path:page>')
def allGets(page):
    return redirect('/')


if __name__ == '__main__':
    app.run()

from datetime import timedelta

from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask import Flask, jsonify, redirect
from sqlalchemy import select

from connection import engine, Locations, Global
from resources.location import Location
from resources.user import UserLogin
from resources.worker import Worker

app = Flask(__name__)
api = Api(app)
app.secret_key = 'sssss'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWTManager(app)


@app.route('/')
def home():
    conn = engine.connect()
    data = conn.execute(select([Global])).fetchall()
    return jsonify({'result': [dict(row) for row in data]})


@app.route('/locations')
def locations():
    conn = engine.connect()
    data = conn.execute(select([Locations])).fetchall()
    return jsonify({'result': [dict(row) for row in data]})


@app.route('/<path:page>')
def allGets(page):
    return redirect('/')


api.add_resource(Location, '/location/')
api.add_resource(UserLogin, '/login/')
api.add_resource(Worker, '/worker/')

if __name__ == '__main__':
    app.run()

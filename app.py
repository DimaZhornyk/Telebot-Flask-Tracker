from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask import Flask, redirect, send_from_directory
from whitenoise import WhiteNoise

from resources.user import UserLogin
from resources.table_names import TableNames, RequiredFields
from resources.tables import Tables, Worker
from flask_cors import CORS

app = Flask(__name__, )
# app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')
api = Api(app)
CORS(app)
app.secret_key = 'sssss'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=7200)
jwt = JWTManager(app)


# @app.route('/')
# def root():
#     return send_from_directory('static', 'index.html')
#     # return app.send_static_file('index.html')


# @app.route('/')
# def root():
#     return send_from_directory('static', 'index.html')
#     # return app.send_static_file('index.html')


api.add_resource(TableNames, '/table_names')
api.add_resource(Tables, '/tables')
api.add_resource(RequiredFields, '/requiredFields')
api.add_resource(UserLogin, '/login/')
api.add_resource(Worker, '/getWorkerById')

@app.route('/')
def root():
    print('lol')
    return send_from_directory('static', 'index.html')
@app.route('/<path:page>')
def allGets(page):
    print(page)
    url = page.rsplit('/',1)
    if(len(url)>=2):
        return send_from_directory('static\\'+url[0],url[1])
    else:
        return send_from_directory('static',url[0])


if __name__ == '__main__':
    app.run()

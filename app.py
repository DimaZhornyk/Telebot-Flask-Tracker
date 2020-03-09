from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask import Flask, redirect, send_from_directory
from resources.user import UserLogin
from resources.table_names import TableNames, RequiredFields
from resources.tables import Tables, Worker
from flask_cors import CORS

app = Flask(__name__,
            static_url_path='',
            static_folder=".\\static",
            )
api = Api(app)
CORS(app)
app.secret_key = 'sssss'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=7200)
jwt = JWTManager(app)

@app.route('/')
def root():
    return send_from_directory('static', 'index.html')
    # return app.send_static_file('index.html')


api.add_resource(TableNames, '/table_names')
api.add_resource(Tables, '/tables')
api.add_resource(RequiredFields, '/requiredFields')
api.add_resource(UserLogin, '/login/')
api.add_resource(Worker, '/getWorkerById')


@app.route('/<path:page>')
def allGets(page):
    return redirect('/')


if __name__ == '__main__':
    app.run()

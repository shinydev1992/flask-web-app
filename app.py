import os
from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash
from extensions import db
from models import User
from auth import auth_blueprint
from sessions import sessions_blueprint
from agendas import agendas_blueprint
from votes import votes_blueprint
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)

# CORS
CORS(app)  # Omogućuje CORS za cijelu aplikaciju

# JWT Config
app.config['JWT_SECRET_KEY'] = '1=6%WRgf4bKxxX5,^ut&$,>n@n0}]5GL'  
jwt = JWTManager(app)

# WebSockets using Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")  # Assuming you want to allow all origins

# Blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(sessions_blueprint, url_prefix='/sessions')
app.register_blueprint(agendas_blueprint, url_prefix='/agendas')
app.register_blueprint(votes_blueprint, url_prefix='/votes')

# Database Config
USERNAME = os.environ.get('DB_USERNAME')
PASSWORD = os.environ.get('DB_PASSWORD')
HOSTNAME = os.environ.get('DB_HOSTNAME')
DBNAME = os.environ.get('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DBNAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    return "Dobrodošli na moju Flask aplikaciju!"

if __name__ == '__main__':
    socketio.run(app, debug=True)  # Use socketio.run instead of app.run

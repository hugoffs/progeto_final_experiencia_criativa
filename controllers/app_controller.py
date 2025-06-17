import os

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError

from controllers.authentication_controller import authentication_
from controllers.error_controller import error_
from controllers.ldev_controller import ldev_
from controllers.locale_controller import locale_
from controllers.log_controller import log_
from controllers.routine_controller import routine_
from controllers.team_controller import team_
from controllers.user_controller import user_
from services.team_service import list_teams # Importar o serviço para listar times
from models.db import db, instance

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder="./views", static_folder="./static", root_path="./")

    app.register_blueprint(authentication_, url_prefix='/api/authentication')
    app.register_blueprint(error_, url_prefix='/api/error')
    app.register_blueprint(ldev_, url_prefix='/api/ldev')
    app.register_blueprint(locale_, url_prefix='/api/locale')
    app.register_blueprint(log_, url_prefix='/api/log')
    app.register_blueprint(routine_, url_prefix='/api/routine')
    app.register_blueprint(team_, url_prefix='/api/team')
    app.register_blueprint(user_, url_prefix='/api/user')

    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance

    # chave secreta para assinar os tokens (guarde em .env)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    # config.py
    app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # ou True, se você lidar com CSRF

    db.init_app(app)
    JWTManager(app)

    template = {
        "swagger": "2.0",
        "info": {
            "title":       "LDev API",
            "description": "A RESTful API for IoT-based irrigation management. Provides JWT-secured endpoints to manage teams and users, define locations and devices, schedule and run irrigation routines, collect sensor data logs, report device errors, and track user activities.",
            "version":     "Indev 0.1.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ]
    }
    Swagger(app, template=template)

    @app.errorhandler(NoAuthorizationError)
    @app.errorhandler(ExpiredSignatureError)
    def handle_jwt_error(e):
        return redirect(url_for('login_page'))

    # -------------------------- Rota de teste do HTML --------------------------
    @app.route('/login', methods=['GET'])
    def login_page():
        return render_template('login.html')

    @app.route('/')
    @jwt_required()
    def index():
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return {'error': 'Acesso negado'}, 403

        current_teams = list_teams()
        return render_template('team.html',  teams=current_teams)

    return app

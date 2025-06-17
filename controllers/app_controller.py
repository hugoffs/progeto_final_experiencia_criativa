import os
from dotenv import load_dotenv

from flasgger import Swagger
from flask import Flask, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError

from flask_socketio import SocketIO  # 🔥 Adiciona o SocketIO

# Blueprints dos controllers
from controllers.authentication_controller import authentication_
from controllers.error_controller import error_
from controllers.ldev_controller import ldev_
from controllers.locale_controller import locale_
from controllers.log_controller import log_
from controllers.routine_controller import routine_
from controllers.team_controller import team_
from controllers.user_controller import user_
from controllers.api_controller import api_
from controllers.mqtt_controller import mqtt_


# Models e serviços
from models.db import db, instance
from services.team_service import list_teams


# 🔧 Carrega variáveis de ambiente
load_dotenv()


def create_app():
    app = Flask(__name__, template_folder="./views", static_folder="./static", root_path="./")

    # 🔗 Configurações principais
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False

    # 🔥 Instancia banco e JWT
    db.init_app(app)
    jwt = JWTManager(app)

    # 🔥 Instancia SocketIO
    socketio = SocketIO(app, cors_allowed_origins="*")

    # 🔗 Registro dos blueprints
    app.register_blueprint(authentication_, url_prefix='/api/authentication')
    app.register_blueprint(error_, url_prefix='/api/error')
    app.register_blueprint(ldev_, url_prefix='/api/ldev')
    app.register_blueprint(locale_, url_prefix='/api/locale')
    app.register_blueprint(log_, url_prefix='/api/log')
    app.register_blueprint(routine_, url_prefix='/api/routine')
    app.register_blueprint(team_, url_prefix='/api/team')
    app.register_blueprint(user_, url_prefix='/api/user')
    app.register_blueprint(api_, url_prefix='/api')
    app.register_blueprint(mqtt_)

    # 🔥 Configuração Swagger
    template = {
        "swagger": "2.0",
        "info": {
            "title": "LDev API",
            "description": "API para gerenciamento de irrigação IoT com JWT e Swagger.",
            "version": "Indev 0.1.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header usando Bearer. Ex: 'Bearer {token}'"
            }
        },
        "security": [{"Bearer": []}]
    }
    Swagger(app, template=template)

    # 🔐 Tratamento de erros de autenticação
    @app.errorhandler(NoAuthorizationError)
    @app.errorhandler(ExpiredSignatureError)
    def handle_jwt_error(e):
        return redirect(url_for('login_page'))

    # --------------------- 🔗 Rotas de navegação ---------------------

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
        return render_template('team.html', teams=current_teams)

    return app, socketio

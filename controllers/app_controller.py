import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_jwt_extended import JWTManager

from controllers.authentication_controller import authentication_
from controllers.error_controller import error_
from controllers.ldev_controller import ldev_
from controllers.locale_conotroller import locale_
from controllers.log_controller import log_
from controllers.routine_controller import routine_
from controllers.team_controller import team_
from controllers.user_controller import user_
from models.db import db, instance


# Classe fake para testar o template
class FakeRoutine:
    def __init__(self, id, name, horario_inicio, horario_fim):
        self.id = id
        self.name = name
        self.horario_inicio = horario_inicio
        self.horario_fim = horario_fim


class FakeUser:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Faketeam: 
    def __init__(self, id ,name):
        self.id = id
        self.name = name

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

    db.init_app(app)
    JWTManager(app)

    # -------------------------- Rota de teste do HTML --------------------------
    @app.route('/')
    def index():

        user = FakeUser(1, "Admin")
        time = [
            Faketeam(1, "time11"),
            Faketeam(2, "time2"),
            Faketeam(3, "time3"),
            Faketeam(4, "time4"),
            Faketeam(5, "time5"),
            Faketeam(6, "time6"),
        ]
        return render_template('team.html',  user_permission=user, teams=time)

    return app

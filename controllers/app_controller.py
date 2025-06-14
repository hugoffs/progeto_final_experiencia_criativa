from flask import Flask, render_template

# -------------------------- Importação dos blueprints --------------------------
from controllers.authentication_controller import authentication_
from controllers.ldev_controller import ldev_
from controllers.locale_conotroller import locale_
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


def create_app():
    app = Flask(__name__, template_folder="./views", static_folder="./static", root_path="./")

    app.register_blueprint(authentication_, url_prefix='/authentication')
    app.register_blueprint(ldev_, url_prefix='/ldev')
    app.register_blueprint(locale_, url_prefix='/locale')
    app.register_blueprint(routine_, url_prefix='/routine')
    app.register_blueprint(team_, url_prefix='/team')
    app.register_blueprint(user_, url_prefix='/user')

    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance

    db.init_app(app)

    # -------------------------- Rota de teste do HTML --------------------------
    @app.route('/')
    def index():
        routines = [
            FakeRoutine(1, "Rotina 1", "08:00", "10:00"),
            FakeRoutine(2, "Rotina 2", "10:00", "12:00"),
            FakeRoutine(3, "Rotina 3", "14:00", "16:00")
        ]

        user = FakeUser(1, "Admin")

        return render_template('routine.html', routines=routines, user=user)

    return app

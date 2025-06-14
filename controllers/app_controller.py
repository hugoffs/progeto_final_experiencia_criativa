from flask import Flask, render_template

# -------------------------- Importação dos blueprints --------------------------
from controllers.authentication_controller import authentication_
from controllers.ldev_controller import ldev_
from controllers.locale_conotroller import locale_
from controllers.routine_controller import routine_
from controllers.team_controller import team_
from controllers.user_controller import user_
from models.db import db, instance

"""
class FakeUser:
    def __init__(self, id, name, time):
        self.id = id
        self.name = name
        self.time = time 
"""


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

    # função onde inicia o app
    @app.route('/')
    def index():
        """
        teste da pagina user.html
        users = [
            FakeUser(1, "João", "time1"),
            FakeUser(2, "Maria", "time2"),
            FakeUser(3, "Carlos", "time3"),
            FakeUser(4, "João", "time1"),
            FakeUser(5, "Maria", "time2"),
            FakeUser(6, "Carlos", "time3"),
            FakeUser(1, "João", "time1"),
            FakeUser(2, "Maria", "time2"),
            FakeUser(3, "Carlos", "time3")
        ]
        """

        return render_template('register_routine.html', user_permission="admin")

    return app

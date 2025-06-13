from flask import Flask, render_template, request
from models.db import db, instance

#-------------------------- Importação dos blueprints --------------------------
from controllers.login_controllers import login_
"""
class FakeUser:
    def __init__(self, id, name, time):
        self.id = id
        self.name = name
        self.time = time 
"""


def create_app():
    app = Flask(__name__, template_folder="./views", static_folder="./static", root_path="./")

    app.register_blueprint(login_, url_prefix='/')

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
from flask import Flask, render_template, request
from models.db import db, instance

#-------------------------- Importação dos blueprints --------------------------
from controllers.login_controllers import login_


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
        return render_template('registrar_usuario.html', user_permission="admin")
    

    return app
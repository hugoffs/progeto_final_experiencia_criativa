from flask import Flask, render_template, request

def create_app():
    app = Flask(__name__, template_folder="./views", static_folder="./static", root_path="./")

    @app.route('/')
    def index():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def login():
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password':
            return render_template('dashboard.html', username=username)
        else:
            return render_template('login.html', error='Invalid credentials')

    @app.route("/recuperar_conta")
    def recuperar_conta():
        return render_template('recuperar_conta.html')

    return app
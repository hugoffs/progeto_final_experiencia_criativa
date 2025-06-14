from flask import Blueprint, request, render_template

authentication_ = Blueprint('authentication', __name__, template_folder="./views", static_folder="./static", root_path="./")

@authentication_.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'admin' and password == 'password':
        return render_template('dashboard.html', username=username)
    else:
        return render_template('login.html', error='Invalid credentials')

@authentication_.route("/recuperar_conta")
def recuperar_conta():
    return render_template('recuperar_conta.html')
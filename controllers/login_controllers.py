from flask import Blueprint, request, render_template

login_ = Blueprint('login', __name__, template_folder="./views", static_folder="./static", root_path="./")



@login_.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'admin' and password == 'password':
        return render_template('dashboard.html', username=username)
    else:
        return render_template('login.html', error='Invalid credentials')

@login_.route("/recuperar_conta")
def recuperar_conta():
    return render_template('recuperar_conta.html')
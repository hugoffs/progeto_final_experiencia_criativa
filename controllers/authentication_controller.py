from flask import Blueprint, request, render_template, jsonify, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, create_access_token, set_access_cookies
from werkzeug.exceptions import BadRequest

from models import User
from services.user_service import list_users

authentication_ = Blueprint('authentication', __name__, template_folder="./views", static_folder="./static", root_path="./")

@authentication_.route('/login/example', methods=['GET'])
@jwt_required()
def protected_page_example():
    # id do usuário que fez a requisição
    current_user_id = get_jwt_identity()

    # por exemplo, você pode verificar claims:
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return {'error': 'Acesso negado'}, 403

    users = list_users()
    return jsonify([u.serialize() for u in users]), 200

    #if username == 'admin' and password == 'password':
        #   return render_template('dashboard.html', username=username)
    #else:
        #   return render_template('login.html', error='Invalid credentials')

@authentication_.route('/login', methods=['POST'])
def login():
    """
     User login endpoint: validates credentials and sets a JWT in an HttpOnly cookie
     ---
     tags:
       - authentication
     consumes:
       - application/json
     parameters:
       - in: body
         name: credentials
         description: User email and password
         required: true
         schema:
           type: object
           required:
             - email
             - password
           properties:
             email:
               type: string
               format: email
               example: user@example.com
             password:
               type: string
               format: password
               example: yourpassword
     responses:
       200:
         description: Login successful; JWT is set in an HttpOnly cookie
         headers:
           Set-Cookie:
             description: |
               HTTP-only cookie named “access_token_cookie” containing the JWT.
               Cookie is marked Secure and SameSite=Lax.
         schema:
           type: object
           properties:
             login:
               type: boolean
               example: true
       400:
         description: Missing email or password
       401:
         description: Invalid credentials
     security: []
     """

    data = request.get_json() or {}
    email    = data.get('email')
    password = data.get('password')
    if not email or not password:
        raise BadRequest("Email e senha são obrigatórios.")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Credenciais inválidas'}), 401

    # aqui você pode inserir claims extras, ex role:
    additional_claims = {'role': user.role}
    access_token = create_access_token(identity=user.id,
                                        additional_claims=additional_claims)
    resp = jsonify({"login": True})
    set_access_cookies(resp, access_token)
    return resp, 200

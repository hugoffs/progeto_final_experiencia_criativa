from flask import Blueprint, request, jsonify, render_template
from werkzeug.exceptions import BadRequest

from services.user_service import list_users, create_user, get_user, update_user, delete_user

user_ = Blueprint('user', __name__, template_folder="./views", static_folder="./static", root_path="./")


@user_.route('/', methods=['GET'])
def list_route():
    users = list_users()
    return jsonify([u.serialize() for u in users]), 200

@user_.route('/', methods=['POST'])
def create_route():
    data = request.get_json() or {}
    for field in ('name', 'email', 'password'):
        if not data.get(field):
            raise BadRequest(f"Campo '{field}' é obrigatório.")
    user = create_user(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'user'),
        team_id=data.get('team_id')
    )
    return jsonify(user.serialize()), 201

@user_.route('/<string:user_id>', methods=['GET'])
def get_route(user_id):
    user = get_user(user_id)
    return jsonify(user.serialize()), 200



@user_.route('/<string:user_id>', methods=['PATCH'])
def update_route(user_id):
    user = get_user(user_id)
    data = request.get_json() or {}
    allowed = {'name', 'email', 'password', 'role', 'team_id'}
    attrs = {k: v for k, v in data.items() if k in allowed}
    if not attrs:
        raise BadRequest("Nenhum campo válido para atualizar.")
    user = update_user(user, **attrs)
    return jsonify(user.serialize()), 200

@user_.route('/<string:user_id>', methods=['DELETE'])
def delete_route(user_id):
    user = get_user(user_id)
    delete_user(user)
    return '', 204

#-------------------- WEB ----------------------------
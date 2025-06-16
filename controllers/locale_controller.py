from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from services.locale_service import delete_locale, get_locale, update_locale, create_locale, list_locales

locale_ = Blueprint('locale', __name__, template_folder="./views", static_folder="./static", root_path="./")

@locale_.route('/', methods=['GET'])
@jwt_required()
def list_route():
    locs = list_locales()
    return jsonify([l.serialize() for l in locs]), 200

@locale_.route('/', methods=['POST'])
@jwt_required()
def create_route():
    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

    data = request.get_json() or {}
    name = data.get('name')
    team_id = data.get('team_id')
    note = data.get('note')
    if not name or not team_id:
        return {'error': 'name e team_id são obrigatórios'}, 400

    loc = create_locale(name=name, team_id=team_id, note=note)
    return jsonify(loc.serialize()), 201

@locale_.route('/<string:locale_id>', methods=['GET'])
@jwt_required()
def get_route(locale_id):
    loc = get_locale(locale_id)
    return jsonify(loc.serialize()), 200

@locale_.route('/<string:locale_id>', methods=['PATCH'])
@jwt_required()
def update_route(locale_id):
    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

    loc = get_locale(locale_id)
    data = request.get_json() or {}
    # Só atualiza campos enviados no payload
    attrs = {}
    if 'name' in data:     attrs['name']     = data['name']
    if 'note' in data:     attrs['note']     = data['note']
    if 'team_id' in data:  attrs['team_id']  = data['team_id']
    if not attrs:
        return {'error': 'Nada para atualizar'}, 400

    loc = update_locale(loc, **attrs)
    return jsonify(loc.serialize()), 200

@locale_.route('/<string:locale_id>', methods=['DELETE'])
@jwt_required()
def delete_route(locale_id):
    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

    loc = get_locale(locale_id)
    delete_locale(loc)
    return '', 204
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from services.error_service import update_error, get_error, delete_error, create_error, list_errors

error_ = Blueprint('error', __name__, template_folder="./views", static_folder="./static", root_path="./")

@error_.route('/', methods=['GET'])
@jwt_required()
def list_route():
    errs = list_errors()
    return jsonify([e.serialize() for e in errs]), 200

@error_.route('/', methods=['POST'])
@jwt_required()
def create_route():
    claims = get_jwt()
    if claims.get('role') != 'device':
        return {'error': 'Acesso negado'}, 403

    data = request.get_json() or {}
    required = ('message', 'ldev_id')
    if not all(field in data for field in required):
        return {'error': f'Campos obrigatórios: {", ".join(required)}'}, 400

    err = create_error(
        message=data['message'],
        ldev_id=data['ldev_id']
    )
    return jsonify(err.serialize()), 201

@error_.route('/<string:error_id>', methods=['GET'])
@jwt_required()
def get_route(error_id):
    claims = get_jwt()
    if claims.get('role') != 'operator':
        return {'error': 'Acesso negado'}, 403

    err = get_error(error_id)
    return jsonify(err.serialize()), 200

@error_.route('/<string:error_id>', methods=['DELETE'])
@jwt_required()
def delete_route(error_id):

    claims = get_jwt()
    if claims.get('role') != 'admin':
        return {'error': 'Acesso negado'}, 403

    err = get_error(error_id)
    delete_error(err)
    return '', 204
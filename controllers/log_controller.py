from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from services.log_service import list_logs, create_log, get_log, update_log, delete_log

log_ = Blueprint('log', __name__, template_folder="./views", static_folder="./static", root_path="./")

@log_.route('/', methods=['GET'])
@jwt_required()
def list_route():
    logs = list_logs()
    return jsonify([l.serialize() for l in logs]), 200

@log_.route('/', methods=['POST'])
@jwt_required()
def create_route():
    claims = get_jwt()
    if claims.get('role') == 'device':
        return {'error': 'Acesso negado'}, 403

    data = request.get_json() or {}
    required = ('humidity', 'temperature', 'ldev_id')
    if not all(field in data for field in required):
        return {'error': f'Campos obrigatórios: {", ".join(required)}'}, 400

    log = create_log(
        humidity=float(data['humidity']),
        temperature=float(data['temperature']),
        ldev_id=data['ldev_id'],
        is_irrigating=bool(data.get('is_irrigating', False))
    )
    return jsonify(log.serialize()), 201

@log_.route('/<string:log_id>', methods=['GET'])
@jwt_required()
def get_route(log_id):
    log = get_log(log_id)
    return jsonify(log.serialize()), 200

@log_.route('/<string:log_id>', methods=['DELETE'])
@jwt_required()
def delete_route(log_id):
    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

    log = get_log(log_id)
    delete_log(log)
    return '', 204
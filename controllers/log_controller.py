from flask import Blueprint, request, jsonify

from services.log_service import list_logs, create_log, get_log, update_log, delete_log

log_ = Blueprint('log', __name__, template_folder="./views", static_folder="./static", root_path="./")

@log_.route('/', methods=['GET'])
def list_route():
    logs = list_logs()
    return jsonify([l.serialize() for l in logs]), 200

@log_.route('/', methods=['POST'])
def create_route():
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
def get_route(log_id):
    log = get_log(log_id)
    return jsonify(log.serialize()), 200

@log_.route('/<string:log_id>', methods=['PATCH'])
def update_route(log_id):
    log = get_log(log_id)
    data = request.get_json() or {}
    attrs = {}
    if 'humidity' in data:      attrs['humidity']      = float(data['humidity'])
    if 'temperature' in data:   attrs['temperature']   = float(data['temperature'])
    if 'is_irrigating' in data: attrs['is_irrigating'] = bool(data['is_irrigating'])
    if 'ldev_id' in data:       attrs['ldev_id']       = data['ldev_id']
    if not attrs:
        return {'error': 'Nenhum campo para atualizar'}, 400

    log = update_log(log, **attrs)
    return jsonify(log.serialize()), 200

@log_.route('/<string:log_id>', methods=['DELETE'])
def delete_route(log_id):
    log = get_log(log_id)
    delete_log(log)
    return '', 204
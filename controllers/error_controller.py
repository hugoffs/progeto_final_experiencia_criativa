from flask import Blueprint, request, jsonify

from services.error_service import update_error, get_error, delete_error, create_error, list_errors

error_ = Blueprint('error', __name__, template_folder="./views", static_folder="./static", root_path="./")

@error_.route('/', methods=['GET'])
def list_route():
    errs = list_errors()
    return jsonify([e.serialize() for e in errs]), 200

@error_.route('/', methods=['POST'])
def create_route():
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
def get_route(error_id):
    err = get_error(error_id)
    return jsonify(err.serialize()), 200

@error_.route('/<string:error_id>', methods=['PATCH'])
def update_route(error_id):
    err = get_error(error_id)
    data = request.get_json() or {}
    attrs = {}
    if 'message' in data:
        attrs['message'] = data['message']
    if 'ldev_id' in data:
        attrs['ldev_id'] = data['ldev_id']
    if not attrs:
        return {'error': 'Nenhum campo para atualizar'}, 400

    err = update_error(err, **attrs)
    return jsonify(err.serialize()), 200

@error_.route('/<string:error_id>', methods=['DELETE'])
def delete_route(error_id):
    err = get_error(error_id)
    delete_error(err)
    return '', 204
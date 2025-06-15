from flask import Blueprint, request, jsonify

from services.ldev_service import create_ldev, list_ldevs, delete_ldev, get_ldev, update_ldev

ldev_ = Blueprint('ldev', __name__, template_folder="./views", static_folder="./static", root_path="./")

@ldev_.route('/', methods=['GET'])
def list_route():
    all_ldevs = list_ldevs()
    return jsonify([l.serialize() for l in all_ldevs]), 200

@ldev_.route('/', methods=['POST'])
def create_route():
    data = request.get_json() or {}
    required = ('name', 'latitude', 'longitude', 'locale_id')
    if not all(field in data for field in required):
        return {'error': f'Campos obrigatórios: {", ".join(required)}'}, 400

    ldev = create_ldev(
        name=data['name'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        locale_id=data['locale_id']
    )
    return jsonify(ldev.serialize()), 201

@ldev_.route('/<string:ldev_id>', methods=['GET'])
def get_route(ldev_id):
    ldev = get_ldev(ldev_id)
    return jsonify(ldev.serialize()), 200

@ldev_.route('/<string:ldev_id>', methods=['PATCH'])
def update_route(ldev_id):
    ldev = get_ldev(ldev_id)
    data = request.get_json() or {}
    attrs = {}
    if 'name' in data:       attrs['name']      = data['name']
    if 'latitude' in data:   attrs['latitude']  = data['latitude']
    if 'longitude' in data:  attrs['longitude'] = data['longitude']
    if 'locale_id' in data:  attrs['locale_id'] = data['locale_id']
    if not attrs:
        return {'error': 'Nenhum campo para atualizar'}, 400

    ldev = update_ldev(ldev, **attrs)
    return jsonify(ldev.serialize()), 200

@ldev_.route('/<string:ldev_id>', methods=['DELETE'])
def delete_route(ldev_id):
    ldev = get_ldev(ldev_id)
    delete_ldev(ldev)
    return '', 204
from datetime import datetime

from flask import Blueprint, request, jsonify

from services.routine_service import update_routine, get_routine, delete_routine, list_routines, create_routine

routine_ = Blueprint('routine', __name__, template_folder="./views", static_folder="./static", root_path="./")

@routine_.route('/', methods=['GET'])
def list_route():
    routines = list_routines()
    return jsonify([r.serialize() for r in routines]), 200

@routine_.route('/', methods=['POST'])
def create_route():
    data = request.get_json() or {}
    # Validações mínimas
    if 'liters_of_water' not in data or 'locale_id' not in data:
        return {'error': 'Campos obrigatórios: liters_of_water, locale_id'}, 400

    # Converte horários se vierem como strings "HH:MM:SS"
    bt = data.get('begin_time')
    et = data.get('end_time')
    begin_time = datetime.strptime(bt, '%H:%M:%S').time() if bt else None
    end_time   = datetime.strptime(et, '%H:%M:%S').time() if et else None

    routine = create_routine(
        temperature      = data.get('temperature'),
        humidity         = data.get('humidity'),
        begin_time       = begin_time,
        end_time         = end_time,
        liters_of_water  = data['liters_of_water'],
        locale_id        = data['locale_id']
    )
    return jsonify(routine.serialize()), 201

@routine_.route('/<string:routine_id>', methods=['GET'])
def get_route(routine_id):
    routine = get_routine(routine_id)
    return jsonify(routine.serialize()), 200

@routine_.route('/<string:routine_id>', methods=['PATCH'])
def update_route(routine_id):
    routine = get_routine(routine_id)
    data = request.get_json() or {}
    attrs = {}

    # Atualiza somente campos passados
    if 'temperature' in data:     attrs['temperature']     = data['temperature']
    if 'humidity' in data:        attrs['humidity']        = data['humidity']
    if 'begin_time' in data:
        attrs['begin_time']   = datetime.strptime(data['begin_time'], '%H:%M:%S').time()
    if 'end_time' in data:
        attrs['end_time']     = datetime.strptime(data['end_time'], '%H:%M:%S').time()
    if 'liters_of_water' in data:
        attrs['liters_of_water'] = data['liters_of_water']
    if 'locale_id' in data:       attrs['locale_id']       = data['locale_id']

    if not attrs:
        return {'error': 'Nada para atualizar'}, 400

    routine = update_routine(routine, **attrs)
    return jsonify(routine.serialize()), 200

@routine_.route('/<string:routine_id>', methods=['DELETE'])
def delete_route(routine_id):
    routine = get_routine(routine_id)
    delete_routine(routine)
    return '', 204
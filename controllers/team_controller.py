from flask import Blueprint, request, jsonify

from services.team_service import list_teams, create_team, get_team, update_team, delete_team

team_ = Blueprint('team', __name__, template_folder="./views", static_folder="./static", root_path="./")

@team_.route('/', methods=['GET'])
def list_route():
    teams = list_teams()
    return jsonify([t.serialize() for t in teams]), 200

@team_.route('/', methods=['POST'])
def create_route():
    data = request.get_json() or {}
    if not data.get('name'):
        return {'error': 'name obrigatório'}, 400
    team = create_team(name=data['name'])
    return jsonify(team.serialize()), 201

@team_.route('/<string:team_id>', methods=['GET'])
def get_route(team_id):
    team = get_team(team_id)
    return jsonify(team.serialize()), 200

@team_.route('/<string:team_id>', methods=['PATCH'])
def update_route(team_id):
    team = get_team(team_id)
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return {'error': 'name obrigatório'}, 400
    team = update_team(team, name=name)
    return jsonify(team.serialize()), 200

@team_.route('/<string:team_id>', methods=['DELETE'])
def delete_route(team_id):
    team = get_team(team_id)
    delete_team(team)
    return '', 204
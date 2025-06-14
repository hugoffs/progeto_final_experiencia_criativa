from flask import Blueprint, request, render_template, jsonify

from services.team_service import list_teams, create_team

team_ = Blueprint('team', __name__, template_folder="./views", static_folder="./static", root_path="./")

@team_.route("/hello", methods=['GET'])
def teste():
    return "hello!"

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
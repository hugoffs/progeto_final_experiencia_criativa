from flask import Blueprint, request, jsonify

from services.team_service import list_teams, create_team, get_team, update_team, delete_team
import uuid

team_ = Blueprint('team', __name__, template_folder="./views", static_folder="./static", root_path="./")

@team_.route('/', methods=['GET'])
def list_route():
    teams = list_teams()
    return jsonify([t.serialize() for t in teams]), 200 

@team_.route('/', methods=['POST'])
def create_route():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return {'error': 'Acesso negado'}, 403

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
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return {'error': 'Acesso negado'}, 403

    team = get_team(team_id)
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return {'error': 'name obrigatório'}, 400
    team = update_team(team, name=name)
    return jsonify(team.serialize()), 200

@team_.route('/<string:team_id>', methods=['DELETE'])
def delete_route(team_id):
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return {'error': 'Acesso negado'}, 403

    team = get_team(team_id)
    if not team:
        return jsonify({"error": "Time não encontrado"}), 404
    try:
        delete_team(team)
        return '', 204 # Sucesso, nenhum conteúdo
    except Exception as e:
        # Idealmente, logar o erro 'e' no servidor
        print(f"Erro ao deletar time {team_id}: {str(e)}") # Log simples para depuração
        return jsonify({"error": "Erro interno ao tentar deletar o time"}), 500


# --------- ROTAS PARA PÁGINAS HTML -----------
@team_.route('/register_team')
def register_team():
    return render_template('register_team.html' )

@team_.route("/add_team", methods=["POST"])
def add_team():
    name = request.form.get("name")
    if not name:
        return "Nome do time é obrigatório", 400
    create_team(name=name) # Corrigido para usar keyword argument
    # Redireciona para a página de listagem de times (rota index)
    return redirect(url_for('index'))

@team_.route("/list_teams")
def tema():
    teams = list_teams()
    # Similar à rota index, precisa de user_permission se team.html depender via base.html
    user_permission = FakeUser(1, "admin") # Placeholder
    return render_template("team.html", teams=teams, user_permission=user_permission)

@team_.route("/edit_team")
def updrate_team():
    id = request.args.get("id")
    team = get_team(id)
    return render_template("update_team.html", team=team)

@team_.route("/update_teams", methods=["POST"])
def update_teams():
    id = request.form.get("id")
    name = request.form.get("name")
    team = get_team(id)
    team = update_team(team, name=name)
    # Redireciona para a página de listagem de times
    return redirect(url_for('index'))


@team_.route("/del_team")
def delete_team_route():
    id = request.args.get("id")
    team = get_team(id)
    delete_team(team)
    return redirect("/api/team/list_teams")
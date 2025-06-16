from flask import Blueprint, request, jsonify, render_template,redirect , url_for
from flask_jwt_extended import jwt_required, get_jwt
from services.team_service import list_teams, create_team, get_team, update_team, delete_team
import uuid

team_ = Blueprint('team', __name__, template_folder="./views", static_folder="./static", root_path="./")

@team_.route('/', methods=['GET'])
@jwt_required()
def list_route():
    """
        Retrieve all teams
        ---
        tags:
          - team
        security:
          - Bearer: []
        responses:
          200:
            description: A JSON array of team objects
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                  name:
                    type: string
                    example: "Engineering Team"
                  created_at:
                    type: string
                    format: date-time
                    example: "2025-06-16T12:34:56Z"
                  updated_at:
                    type: string
                    format: date-time
                    example: "2025-06-16T13:45:00Z"
          401:
            description: Missing or invalid JWT token
        """
    teams = list_teams()
    return jsonify([t.serialize() for t in teams]), 200 

@team_.route('/', methods=['POST'])
@jwt_required()
def create_route():
    """
        Create a new team (admin only)
        ---
        tags:
          - team
        security:
          - Bearer: []
        consumes:
          - application/json
        parameters:
          - in: body
            name: team
            description: Team data to create
            required: true
            schema:
              type: object
              required:
                - name
              properties:
                name:
                  type: string
                  example: "Engineering Team"
        responses:
          201:
            description: Team created successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                name:
                  type: string
                  example: "Engineering Team"
                created_at:
                  type: string
                  format: date-time
                  example: "2025-06-16T12:34:56Z"
                updated_at:
                  type: string
                  format: date-time
                  example: "2025-06-16T13:45:00Z"
          400:
            description: Missing required field (name)
          401:
            description: Missing or invalid JWT token
          403:
            description: Forbidden – only admins may create teams
        """

    claims = get_jwt()
    if claims.get('role') != 'admin':
        return {'error': 'Acesso negado'}, 403

    data = request.get_json() or {}
    if not data.get('name'):
        return {'error': 'name obrigatório'}, 400
    team = create_team(name=data['name'])
    return jsonify(team.serialize()), 201

@team_.route('/<string:team_id>', methods=['GET'])
@jwt_required()
def get_route(team_id):
    """
        Retrieve a specific team by ID
        ---
        tags:
          - team
        security:
          - Bearer: []
        parameters:
          - name: team_id
            in: path
            type: string
            required: true
            description: UUID of the team to retrieve
        responses:
          200:
            description: Team object returned successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                name:
                  type: string
                  example: "Engineering Team"
                created_at:
                  type: string
                  format: date-time
                  example: "2025-06-16T12:34:56Z"
                updated_at:
                  type: string
                  format: date-time
                  example: "2025-06-16T13:45:00Z"
          401:
            description: Missing or invalid JWT token
          404:
            description: Team not found
        """

    team = get_team(team_id)
    return jsonify(team.serialize()), 200

@team_.route('/<string:team_id>', methods=['PATCH'])
@jwt_required()
def update_route(team_id):
    """
        Update a team’s name by ID (admin only)
        ---
        tags:
          - team
        security:
          - Bearer: []
        consumes:
          - application/json
        parameters:
          - name: team_id
            in: path
            type: string
            required: true
            description: UUID of the team to update
          - in: body
            name: payload
            description: Fields to update (only “name”)
            required: true
            schema:
              type: object
              required:
                - name
              properties:
                name:
                  type: string
                  example: "New Team Name"
        responses:
          200:
            description: Team updated successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                name:
                  type: string
                  example: "New Team Name"
                created_at:
                  type: string
                  format: date-time
                updated_at:
                  type: string
                  format: date-time
          400:
            description: Missing required field (name)
          401:
            description: Missing or invalid JWT token
          403:
            description: Forbidden – only admins may update teams
          404:
            description: Team not found
        """

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
@jwt_required()
def delete_route(team_id):
    """
    Delete a team by ID (admin only)
    ---
    tags:
      - team
    security:
      - Bearer: []
    parameters:
      - name: team_id
        in: path
        type: string
        required: true
        description: UUID of the team to delete
    responses:
      204:
        description: Team deleted successfully (no content)
      401:
        description: Missing or invalid JWT token
      403:
        description: Forbidden – only admins may delete teams
      404:
        description: Team not found
      500:
        description: Internal server error while attempting to delete the team
    """

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
    return render_template("team.html", teams=teams, )

@team_.route("/edit_team")
def update_team():
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
from flask import Blueprint, request, jsonify,render_template, redirect
from flask_jwt_extended import jwt_required, get_jwt

from services.locale_service import delete_locale, get_locale, update_locale, create_locale, list_locales
from services.team_service import list_teams

locale_ = Blueprint('locale', __name__, template_folder="./views", static_folder="./static", root_path="./")

@locale_.route('/', methods=['GET'])
@jwt_required()
def list_route():
    """
        Retrieve all locales
        ---
        tags:
          - locale
        security:
          - Bearer: []
        responses:
          200:
            description: A JSON array of locale objects
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
                    example: "Main Farm"
                  note:
                    type: string
                    example: "North Wing"
                  team_id:
                    type: string
                    example: "1b645389-2473-446f-8f22-6f6b72a4a516"
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

    locs = list_locales()
    return jsonify([l.serialize() for l in locs]), 200

@locale_.route('/', methods=['POST'])
@jwt_required()
def create_route():
    """
        Create a new locale (operator or admin only)
        ---
        tags:
          - locale
        security:
          - Bearer: []
        consumes:
          - application/json
        parameters:
          - in: body
            name: locale
            description: Locale details to create
            required: true
            schema:
              type: object
              required:
                - name
                - team_id
              properties:
                name:
                  type: string
                  example: "Main Farm"
                team_id:
                  type: string
                  example: "1b645389-2473-446f-8f22-6f6b72a4a516"
                note:
                  type: string
                  example: "North Wing"
        responses:
          201:
            description: Locale created successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                name:
                  type: string
                  example: "Main Farm"
                note:
                  type: string
                  example: "North Wing"
                team_id:
                  type: string
                  example: "1b645389-2473-446f-8f22-6f6b72a4a516"
                created_at:
                  type: string
                  format: date-time
                  example: "2025-06-16T12:34:56Z"
                updated_at:
                  type: string
                  format: date-time
                  example: "2025-06-16T13:45:00Z"
          400:
            description: Missing required fields (name and team_id)
          401:
            description: Missing or invalid JWT token
          403:
            description: Forbidden – users with role "user" may not create locales
        """

    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

    data = request.get_json() or {}
    name = data.get('name')
    team_id = data.get('team_id')
    note = data.get('note')
    if not name or not team_id:
        return {'error': 'name e team_id são obrigatórios'}, 400

    loc = create_locale(name=name, team_id=team_id, note=note)
    return jsonify(loc.serialize()), 201

@locale_.route('/<string:locale_id>', methods=['GET'])
@jwt_required()
def get_route(locale_id):
    """
    Retrieve a specific locale by ID
    ---
    tags:
      - locale
    security:
      - Bearer: []
    parameters:
      - name: locale_id
        in: path
        type: string
        required: true
        description: UUID of the locale to retrieve
    responses:
      200:
        description: Locale object returned successfully
        schema:
          type: object
          properties:
            id:
              type: string
              example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            name:
              type: string
              example: "Main Farm"
            note:
              type: string
              example: "North Wing"
            team_id:
              type: string
              example: "1b645389-2473-446f-8f22-6f6b72a4a516"
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
        description: Locale not found
    """

    loc = get_locale(locale_id)
    return jsonify(loc.serialize()), 200

@locale_.route('/<string:locale_id>', methods=['PATCH'])
@jwt_required()
def update_route(locale_id):
    """
        Update an existing locale by ID (operator or admin only)
        ---
        tags:
          - locale
        security:
          - Bearer: []
        consumes:
          - application/json
        parameters:
          - name: locale_id
            in: path
            description: UUID of the locale to update
            required: true
            type: string
          - in: body
            name: updates
            description: Fields to update (any of name, note, team_id)
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: "Updated Farm Name"
                note:
                  type: string
                  example: "Updated note"
                team_id:
                  type: string
                  example: "1b645389-2473-446f-8f22-6f6b72a4a516"
        responses:
          200:
            description: Locale updated successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                name:
                  type: string
                note:
                  type: string
                team_id:
                  type: string
                created_at:
                  type: string
                  format: date-time
                updated_at:
                  type: string
                  format: date-time
          400:
            description: No fields provided to update
          401:
            description: Missing or invalid JWT token
          403:
            description: Forbidden – users with role "user" may not update locales
          404:
            description: Locale not found
        """

    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

    loc = get_locale(locale_id)
    data = request.get_json() or {}
    # Só atualiza campos enviados no payload
    attrs = {}
    if 'name' in data:     attrs['name']     = data['name']
    if 'note' in data:     attrs['note']     = data['note']
    if 'team_id' in data:  attrs['team_id']  = data['team_id']
    if not attrs:
        return {'error': 'Nada para atualizar'}, 400

    loc = update_locale(loc, **attrs)
    return jsonify(loc.serialize()), 200

@locale_.route('/<string:locale_id>', methods=['DELETE'])
@jwt_required()
def delete_route(locale_id):
    """
    Delete a locale by ID (operator or admin only)
    ---
    tags:
      - locale
    security:
      - Bearer: []
    parameters:
      - name: locale_id
        in: path
        type: string
        required: true
        description: UUID of the locale to delete
    responses:
      204:
        description: Locale deleted successfully (no content)
      401:
        description: Missing or invalid JWT token
      403:
        description: Forbidden – users with role "user" may not delete locales
      404:
        description: Locale not found
    """

    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

    loc = get_locale(locale_id)
    delete_locale(loc)
    return '', 204

#------------ WEB -------------------------
@locale_.route("/list_locale")
def list_locales_route():
    locales = list_locales()
    return render_template("locale.html", locales= locales)

@locale_.route('/register_locale')
def register_locale():
    teams = list_teams()
    return render_template('register_locale.html', teams= teams)

@locale_.route('/add_locale', methods=['POST'])
def add_locale():
    name = request.form.get('name')
    team_id = request.form.get('team_id')
    note = request.form.get('note')
    if not name:
      return "Nome do time é obrigatório", 400 
    
    create_locale(name=name, team_id=team_id, note=note)
    return redirect("/api/locale/lista_locais")

@locale_.route("/edit_locale")
def edit_locale():
    id = request.args.get("id")
    locale = get_locale(id)
    teams = list_teams()
    return render_template("update_locale.html", locale=locale, teams=teams)

@locale_.route("/update_locale", methods=["POST"])
def update_locale_route():
    id = request.form.get("id")
    name = request.form.get("name")
    team_id = request.form.get("team_id")
    note = request.form.get("note")

    locale = get_locale(id)
    update_locale(locale, name=name, team_id=team_id, note=note)
    return redirect("/api/locale/lista_locais")

@locale_.route("/del_loacle")
def del_locale():
    id = request.args.get("id")
    locale = get_locale(id)
    delete_locale(locale)
    return redirect("/api/locale/lista_locais")
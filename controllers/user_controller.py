from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import jwt_required, get_jwt

from services.user_service import list_users, create_user, get_user, update_user, delete_user

user_ = Blueprint('user', __name__, template_folder="./views", static_folder="./static", root_path="./")


@user_.route('/', methods=['GET'])
@jwt_required()
def list_route():
    """
        Retrieve a list of all users (admin only)
        ---
        tags:
          - user
        security:
          - Bearer: []
        responses:
          200:
            description: A JSON array of user objects
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
                    example: "John Doe"
                  email:
                    type: string
                    format: email
                    example: "johndoe@example.com"
                  role:
                    type: string
                    enum: ["admin", "operator", "user"]
                    example: "user"
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
          403:
            description: Forbidden – only users with the "admin" role may access this endpoint
        """

    claims = get_jwt()
    if claims.get('role') != 'admin':
        return {'error': 'Acesso negado'}, 403

    users = list_users()
    return jsonify([u.serialize() for u in users]), 200

@user_.route('/', methods=['POST'])
@jwt_required()
def create_route():
    """
        Create a new user (admin only)
        ---
        tags:
          - user
        security:
          - Bearer: []
        consumes:
          - application/json
        parameters:
          - in: body
            name: user
            description: User details to create
            required: true
            schema:
              type: object
              required:
                - name
                - email
                - password
              properties:
                name:
                  type: string
                  example: "Jane Doe"
                email:
                  type: string
                  format: email
                  example: "jane.doe@example.com"
                password:
                  type: string
                  format: password
                  example: "StrongP@ssw0rd"
                role:
                  type: string
                  enum: ["admin", "operator", "user"]
                  example: "user"
                team_id:
                  type: string
                  example: "1b645389-2473-446f-8f22-6f6b72a4a516"
        responses:
          201:
            description: User created successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                name:
                  type: string
                  example: "Jane Doe"
                email:
                  type: string
                  format: email
                  example: "jane.doe@example.com"
                role:
                  type: string
                  enum: ["admin", "operator", "user"]
                  example: "user"
                team_id:
                  type: string
                  example: "1b645389-2473-446f-8f22-6f6b72a4a516"
                created_at:
                  type: string
                  format: date-time
                updated_at:
                  type: string
                  format: date-time
          400:
            description: Missing or invalid fields
          401:
            description: Missing or invalid JWT token
          403:
            description: Forbidden – only admins may create users
        """

    claims = get_jwt()
    if claims.get('role') != 'admin':
        return {'error': 'Acesso negado'}, 403

    data = request.get_json() or {}
    for field in ('name', 'email', 'password'):
        if not data.get(field):
            raise BadRequest(f"Campo '{field}' é obrigatório.")
    user = create_user(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'user'),
        team_id=data.get('team_id')
    )
    return jsonify(user.serialize()), 201

@user_.route('/<string:user_id>', methods=['GET'])
@jwt_required()
def get_route(user_id):
    """
        Retrieve a single user by ID (admin only)
        ---
        tags:
          - user
        security:
          - Bearer: []
        parameters:
          - name: user_id
            in: path
            type: string
            required: true
            description: UUID of the user to retrieve
        responses:
          200:
            description: User object returned successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                name:
                  type: string
                  example: "Alice Smith"
                email:
                  type: string
                  format: email
                  example: "alice.smith@example.com"
                role:
                  type: string
                  enum: ["admin", "operator", "user"]
                  example: "operator"
                team_id:
                  type: string
                  example: "1b645389-2473-446f-8f22-6f6b72a4a516"
                created_at:
                  type: string
                  format: date-time
                updated_at:
                  type: string
                  format: date-time
          401:
            description: Missing or invalid JWT token
          403:
            description: Forbidden – only admins may access this endpoint
          404:
            description: User not found
        """
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return {'error': 'Acesso negado'}, 403

    user = get_user(user_id)
    return jsonify(user.serialize()), 200



@user_.route('/<string:user_id>', methods=['PATCH'])
@jwt_required()
def update_route(user_id):
    """
        Update an existing user by ID (admin only)
        ---
        tags:
          - user
        security:
          - Bearer: []
        parameters:
          - name: user_id
            in: path
            description: UUID of the user to update
            required: true
            type: string
          - in: body
            name: updates
            description: Fields to update (any of name, email, password, role, team_id)
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: "Updated Name"
                email:
                  type: string
                  format: email
                  example: "updated.email@example.com"
                password:
                  type: string
                  format: password
                  example: "NewP@ssw0rd"
                role:
                  type: string
                  enum:
                    - admin
                    - operator
                    - user
                  example: "operator"
                team_id:
                  type: string
                  example: "1b645389-2473-446f-8f22-6f6b72a4a516"
                  
        responses:
          200:
            description: User updated successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                name:
                  type: string
                email:
                  type: string
                  format: email
                role:
                  type: string
                  enum: ["admin","operator","user"]
                team_id:
                  type: string
                created_at:
                  type: string
                  format: date-time
                updated_at:
                  type: string
                  format: date-time
          400:
            description: No valid fields provided or invalid input
          401:
            description: Missing or invalid JWT token
          403:
            description: Forbidden – only admins may update users
          404:
            description: User not found
        """

    claims = get_jwt()
    if claims.get('role') != 'admin':
        return {'error': 'Acesso negado'}, 403

    user = get_user(user_id)
    data = request.get_json() or {}
    allowed = {'name', 'email', 'password', 'role', 'team_id'}
    attrs = {k: v for k, v in data.items() if k in allowed}
    if not attrs:
        raise BadRequest("Nenhum campo válido para atualizar.")
    user = update_user(user, **attrs)
    return jsonify(user.serialize()), 200

@user_.route('/<string:user_id>', methods=['DELETE'])
@jwt_required()
def delete_route(user_id):
    """
    Delete a user by ID (admin only)
    ---
    tags:
      - user
    security:
      - Bearer: []
    parameters:
      - name: user_id
        in: path
        description: UUID of the user to delete
        required: true
        type: string
    responses:
      204:
        description: User deleted successfully (no content)
      401:
        description: Missing or invalid JWT token
      403:
        description: Forbidden – only admins may delete users
      404:
        description: User not found
    """

    claims = get_jwt()
    if claims.get('role') != 'admin':
        return {'error': 'Acesso negado'}, 403

    user = get_user(user_id)
    delete_user(user)
    return '', 204

#-------------------- WEB ----------------------------
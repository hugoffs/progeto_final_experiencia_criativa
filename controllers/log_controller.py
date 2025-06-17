from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt

from services.log_service import list_logs, create_log, get_log, update_log, delete_log

log_ = Blueprint('log', __name__, template_folder="./views", static_folder="./static", root_path="./")

@log_.route('/', methods=['GET'])
@jwt_required()
def list_route():
    """
        List all sensor logs
        ---
        tags:
          - log
        security:
          - Bearer: []
        responses:
          200:
            description: A JSON array of log entries
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                  humidity:
                    type: number
                    format: float
                    example: 45.3
                  temperature:
                    type: number
                    format: float
                    example: 22.7
                  is_irrigating:
                    type: boolean
                    example: false
                  created_at:
                    type: string
                    format: date-time
                    example: "2025-06-16T12:34:56Z"
                  ldev_id:
                    type: string
                    example: "1b645389-2473-446f-8f22-6f6b72a4a516"
          401:
            description: Missing or invalid JWT token
        """

    logs = list_logs()
    return jsonify([l.serialize() for l in logs]), 200

@log_.route('/', methods=['POST'])
@jwt_required()
def create_route():
    """
        Create a new sensor log entry (operator or admin only)
        ---
        tags:
          - log
        security:
          - Bearer: []
        consumes:
          - application/json
        parameters:
          - in: body
            name: log
            description: Log entry details
            required: true
            schema:
              type: object
              required:
                - humidity
                - temperature
                - ldev_id
              properties:
                humidity:
                  type: number
                  format: float
                  example: 45.3
                temperature:
                  type: number
                  format: float
                  example: 22.7
                is_irrigating:
                  type: boolean
                  example: false
                ldev_id:
                  type: string
                  description: UUID of the device reporting this log
                  example: "1b645389-2473-446f-8f22-6f6b72a4a516"
        responses:
          201:
            description: Log entry created successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                humidity:
                  type: number
                  format: float
                temperature:
                  type: number
                  format: float
                is_irrigating:
                  type: boolean
                created_at:
                  type: string
                  format: date-time
                ldev_id:
                  type: string
          400:
            description: Missing required fields (humidity, temperature, ldev_id)
          401:
            description: Missing or invalid JWT token
          403:
            description: Forbidden – devices may not create log entries
        """

    claims = get_jwt()
    if claims.get('role') == 'device':
        return {'error': 'Acesso negado'}, 403

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
@jwt_required()
def get_route(log_id):
    """
        Retrieve a specific log entry by ID
        ---
        tags:
          - log
        security:
          - Bearer: []
        parameters:
          - name: log_id
            in: path
            type: string
            required: true
            description: UUID of the log entry to retrieve
        responses:
          200:
            description: Log entry returned successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                humidity:
                  type: number
                  format: float
                  example: 45.3
                temperature:
                  type: number
                  format: float
                  example: 22.7
                is_irrigating:
                  type: boolean
                  example: false
                created_at:
                  type: string
                  format: date-time
                  example: "2025-06-16T12:34:56Z"
                ldev_id:
                  type: string
                  example: "1b645389-2473-446f-8f22-6f6b72a4a516"
          401:
            description: Missing or invalid JWT token
          404:
            description: Log entry not found
        """

    log = get_log(log_id)
    return jsonify(log.serialize()), 200

@log_.route('/<string:log_id>', methods=['DELETE'])
@jwt_required()
def delete_route(log_id):
    """
        Delete a log entry by ID (operator or admin only)
        ---
        tags:
          - log
        security:
          - Bearer: []
        parameters:
          - name: log_id
            in: path
            type: string
            required: true
            description: UUID of the log entry to delete
        responses:
          204:
            description: Log entry deleted successfully (no content)
          401:
            description: Missing or invalid JWT token
          403:
            description: Forbidden – users with role "user" may not delete logs
          404:
            description: Log entry not found
        """

    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

    log = get_log(log_id)
    delete_log(log)
    return '', 204

#--------- web --------------------
@log_.route("/dados_temporeal")
def dados_temporeal():
    return render_template("dados_temporeal.html")
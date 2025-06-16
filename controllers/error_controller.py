from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from services.error_service import update_error, get_error, delete_error, create_error, list_errors

error_ = Blueprint('error', __name__, template_folder="./views", static_folder="./static", root_path="./")

@error_.route('/', methods=['GET'])
@jwt_required()
def list_route():
    """
    List all device error logs (operator or admin only)
    ---
    tags:
      - error
    security:
      - Bearer: []
    responses:
      200:
        description: A JSON array of error log objects
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
              message:
                type: string
                example: "Sensor malfunction detected"
              created_at:
                type: string
                format: date-time
                example: "2025-06-16T12:34:56Z"
              ldev_id:
                type: string
                example: "1b645389-2473-446f-8f22-6f6b72a4a516"
      401:
        description: Missing or invalid JWT token
      403:
        description: Forbidden – users with role "user" may not access this endpoint
    """
    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

    errs = list_errors()
    return jsonify([e.serialize() for e in errs]), 200

@error_.route('/', methods=['POST'])
@jwt_required()
def create_route():
    """
    Create a new device error log (device only)
    ---
    tags:
      - error
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: error_log
        description: Error log details from device
        required: true
        schema:
          type: object
          required:
            - message
            - ldev_id
          properties:
            message:
              type: string
              example: "Sensor overheating detected"
            ldev_id:
              type: string
              description: UUID of the device generating the error
              example: "1b645389-2473-446f-8f22-6f6b72a4a516"
    responses:
      201:
        description: Error log created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            message:
              type: string
              example: "Sensor overheating detected"
            created_at:
              type: string
              format: date-time
              example: "2025-06-16T12:34:56Z"
            ldev_id:
              type: string
              example: "1b645389-2473-446f-8f22-6f6b72a4a516"
      400:
        description: Missing required fields (message, ldev_id)
      401:
        description: Missing or invalid JWT token
      403:
        description: Forbidden – only devices may create error logs
    """
    claims = get_jwt()
    if claims.get('role') != 'device':
        return {'error': 'Acesso negado'}, 403

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
@jwt_required()
def get_route(error_id):
    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

    err = get_error(error_id)
    return jsonify(err.serialize()), 200

@error_.route('/<string:error_id>', methods=['DELETE'])
@jwt_required()
def delete_route(error_id):
    """
       Delete an error log by ID (admin only)
       ---
       tags:
         - error
       security:
         - Bearer: []
       parameters:
         - name: error_id
           in: path
           type: string
           required: true
           description: UUID of the error log to delete
       responses:
         204:
           description: Error log deleted successfully (no content)
         401:
           description: Missing or invalid JWT token
         403:
           description: Forbidden – only admins may delete error logs
         404:
           description: Error log not found
       """

    claims = get_jwt()
    if claims.get('role') != 'admin':
        return {'error': 'Acesso negado'}, 403

    err = get_error(error_id)
    delete_error(err)
    return '', 204
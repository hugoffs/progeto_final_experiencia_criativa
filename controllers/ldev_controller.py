from flask import Blueprint, request, jsonify, render_template,redirect
from flask_jwt_extended import jwt_required, get_jwt

from services.ldev_service import create_ldev, list_ldevs, delete_ldev, get_ldev, update_ldev
from services.locale_service import list_locales

ldev_ = Blueprint('ldev', __name__, template_folder="./views", static_folder="./static", root_path="./")

@ldev_.route('/', methods=['GET'])
@jwt_required()
def list_route():
    """
        Retrieve all IoT devices
        ---
        tags:
          - ldev
        security:
          - Bearer: []
        responses:
          200:
            description: A JSON array of LDev objects
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
                    example: "Device A"
                  latitude:
                    type: number
                    format: double
                    example: -23.550520
                  longitude:
                    type: number
                    format: double
                    example: -46.633308
                  locale_id:
                    type: string
                    example: "1b645389-2473-446f-8f22-6f6b72a4a516"
          401:
            description: Missing or invalid JWT token
        """

    all_ldevs = list_ldevs()
    return jsonify([l.serialize() for l in all_ldevs]), 200

@ldev_.route('/', methods=['POST'])
@jwt_required()
def create_route():
    """
        Retrieve all IoT devices
        ---
        tags:
          - ldev
        security:
          - Bearer: []
        responses:
          200:
            description: A JSON array of LDev objects
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
                    example: "Device A"
                  latitude:
                    type: number
                    format: double
                    example: -23.550520
                  longitude:
                    type: number
                    format: double
                    example: -46.633308
                  locale_id:
                    type: string
                    example: "1b645389-2473-446f-8f22-6f6b72a4a516"
          401:
            description: Missing or invalid JWT token
        """

    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

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
@jwt_required()
def get_route(ldev_id):
    ldev = get_ldev(ldev_id)
    return jsonify(ldev.serialize()), 200

@ldev_.route('/<string:ldev_id>', methods=['PATCH'])
@jwt_required()
def update_route(ldev_id):
    """
        Retrieve a specific IoT device by ID
        ---
        tags:
          - ldev
        security:
          - Bearer: []
        parameters:
          - name: ldev_id
            in: path
            type: string
            required: true
            description: UUID of the device to retrieve
        responses:
          200:
            description: Device object returned successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                name:
                  type: string
                  example: "Irrigation Sensor"
                latitude:
                  type: number
                  format: double
                  example: -23.550520
                longitude:
                  type: number
                  format: double
                  example: -46.633308
                locale_id:
                  type: string
                  example: "1b645389-2473-446f-8f22-6f6b72a4a516"
          401:
            description: Missing or invalid JWT token
          404:
            description: Device not found
        """

    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

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
@jwt_required()
def delete_route(ldev_id):
    """
        Delete an IoT device by ID (operator or admin only)
        ---
        tags:
          - ldev
        security:
          - Bearer: []
        parameters:
          - name: ldev_id
            in: path
            type: string
            required: true
            description: UUID of the device to delete
        responses:
          204:
            description: Device deleted successfully (no content)
          401:
            description: Missing or invalid JWT token
          403:
            description: Forbidden – users with role "user" may not delete devices
          404:
            description: Device not found
        """

    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

    ldev = get_ldev(ldev_id)
    delete_ldev(ldev)
    return '', 204

#----------- WEB ---------------------------
@ldev_.route("/list_devices")
def list_devices():
    all_ldevs = list_ldevs()
    return render_template("devices.html", ldevs=all_ldevs)

@ldev_.route("/registre_device")
def registre_device():
    locales = list_locales()
    return render_template("registre_device.html", locales=locales)

@ldev_.route("/add_ldev", methods=['POST'])
def add_device():
    # Para dados enviados via formulário, use request.form
    name = request.form.get('name')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    locale_id = request.form.get('locale_id')

    if not locale_id:
        return {"error": "locale_id é obrigatório."}, 400

    try:
        device = create_ldev(name=name, latitude=latitude, longitude=longitude, locale_id=locale_id)
    except ValueError as e:
        return {"error": str(e)}, 400

    # Redirecionar para a página que lista os dispositivos
    return redirect("/api/ldev/list_devices")

@ldev_.route("/edit_device")
def edit_device():
  id = request.args.get("id")
  ldev = get_ldev(id)
  locales = list_locales()
  return render_template("update_device.html", ldevs=ldev, locales=locales)

@ldev_.route("/update_device", methods=['POST'])
def update_device():
    id = request.form.get("id")
    name = request.form.get('name')
    logi = request.form.get('longitude')
    lati = request.form.get('latitude')
    locale_id = request.form.get('locale_id')
    ldev = get_ldev(id)
    ldev = update_ldev(ldev=ldev, name=name, longitude=logi, latitude=lati, locale_id=locale_id)
    return redirect("/api/ldev/list_devices")

@ldev_.route("/del_device")
def del_ldev():
    id = request.args.get("id")
    ldev = get_ldev(id)
    delete_ldev(ldev)
    return redirect("/api/ldev/list_devices")
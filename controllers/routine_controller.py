from datetime import datetime

from flask import Blueprint, request, jsonify, render_template, redirect, session
from flask_jwt_extended import jwt_required, get_jwt

from services.locale_service import list_locales
from services.routine_service import update_routine, get_routine, delete_routine, list_routines, create_routine

routine_ = Blueprint('routine', __name__, template_folder="./views", static_folder="./static", root_path="./")

@routine_.route('/', methods=['GET'])
@jwt_required()
def list_route():
    """
        List all irrigation routines
        ---
        tags:
          - routine
        security:
          - Bearer: []
        responses:
          200:
            description: A JSON array of routine objects
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                  temperature:
                    type: number
                    format: float
                    example: 25.5
                  humidity:
                    type: number
                    format: float
                    example: 60.0
                  begin_time:
                    type: string
                    format: time
                    example: "08:00:00"
                  end_time:
                    type: string
                    format: time
                    example: "10:00:00"
                  liters_of_water:
                    type: integer
                    example: 100
                  locale_id:
                    type: string
                    example: "1b645389-2473-446f-8f22-6f6b72a4a516"
                  created_at:
                    type: string
                    format: date-time
                    example: "2025-06-16T08:00:00Z"
                  updated_at:
                    type: string
                    format: date-time
                    example: "2025-06-16T09:00:00Z"
          401:
            description: Missing or invalid JWT token
        """

    routines = list_routines()
    return jsonify([r.serialize() for r in routines]), 200

@routine_.route('/', methods=['POST'])
@jwt_required()
def create_route():
    """
        Create a new irrigation routine (operator or admin only)
        ---
        tags:
          - routine
        security:
          - Bearer: []
        consumes:
          - application/json
        parameters:
          - in: body
            name: routine
            description: Routine details to create
            required: true
            schema:
              type: object
              required:
                - liters_of_water
                - locale_id
              properties:
                temperature:
                  type: number
                  format: float
                  example: 25.5
                humidity:
                  type: number
                  format: float
                  example: 60.0
                begin_time:
                  type: string
                  format: time
                  example: "08:00:00"
                end_time:
                  type: string
                  format: time
                  example: "10:00:00"
                liters_of_water:
                  type: integer
                  example: 100
                locale_id:
                  type: string
                  example: "1b645389-2473-446f-8f22-6f6b72a4a516"
        responses:
          201:
            description: Routine created successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                temperature:
                  type: number
                  format: float
                humidity:
                  type: number
                  format: float
                begin_time:
                  type: string
                  format: time
                end_time:
                  type: string
                  format: time
                liters_of_water:
                  type: integer
                locale_id:
                  type: string
                created_at:
                  type: string
                  format: date-time
                updated_at:
                  type: string
                  format: date-time
          400:
            description: Missing required fields (liters_of_water, locale_id)
          401:
            description: Missing or invalid JWT token
          403:
            description: Forbidden – users with role "user" may not create routines
        """

    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

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
@jwt_required()
def get_route(routine_id):
    """
        Retrieve a specific irrigation routine by ID
        ---
        tags:
          - routine
        security:
          - Bearer: []
        parameters:
          - name: routine_id
            in: path
            type: string
            required: true
            description: UUID of the routine to retrieve
        responses:
          200:
            description: Routine object returned successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                temperature:
                  type: number
                  format: float
                  example: 25.5
                humidity:
                  type: number
                  format: float
                  example: 60.0
                begin_time:
                  type: string
                  format: time
                  example: "08:00:00"
                end_time:
                  type: string
                  format: time
                  example: "10:00:00"
                liters_of_water:
                  type: integer
                  example: 100
                locale_id:
                  type: string
                  example: "1b645389-2473-446f-8f22-6f6b72a4a516"
                created_at:
                  type: string
                  format: date-time
                  example: "2025-06-16T08:00:00Z"
                updated_at:
                  type: string
                  format: date-time
                  example: "2025-06-16T09:00:00Z"
          401:
            description: Missing or invalid JWT token
          404:
            description: Routine not found
        """

    routine = get_routine(routine_id)
    return jsonify(routine.serialize()), 200

@routine_.route('/<string:routine_id>', methods=['PATCH'])
@jwt_required()
def update_route(routine_id):
    """
        Update an existing irrigation routine by ID (operator or admin only)
        ---
        tags:
          - routine
        security:
          - Bearer: []
        parameters:
          - name: routine_id
            in: path
            type: string
            required: true
            description: UUID of the routine to update
          - in: body
            name: updates
            description: Fields to update (any combination of temperature, humidity, begin_time, end_time, liters_of_water, locale_id)
            required: true
            schema:
              type: object
              properties:
                temperature:
                  type: number
                  format: float
                  example: 26.0
                humidity:
                  type: number
                  format: float
                  example: 55.0
                begin_time:
                  type: string
                  format: time
                  example: "07:30:00"
                end_time:
                  type: string
                  format: time
                  example: "09:30:00"
                liters_of_water:
                  type: integer
                  example: 120
                locale_id:
                  type: string
                  example: "1b645389-2473-446f-8f22-6f6b72a4a516"
        responses:
          200:
            description: Routine updated successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                temperature:
                  type: number
                  format: float
                humidity:
                  type: number
                  format: float
                begin_time:
                  type: string
                  format: time
                end_time:
                  type: string
                  format: time
                liters_of_water:
                  type: integer
                locale_id:
                  type: string
                created_at:
                  type: string
                  format: date-time
                updated_at:
                  type: string
                  format: date-time
          400:
            description: No valid fields provided for update
          401:
            description: Missing or invalid JWT token
          403:
            description: Forbidden – users with role "user" may not update routines
          404:
            description: Routine not found
        """

    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

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
@jwt_required()
def delete_route(routine_id):
    """
        Delete an irrigation routine by ID (operator or admin only)
        ---
        tags:
          - routine
        security:
          - Bearer: []
        parameters:
          - name: routine_id
            in: path
            type: string
            required: true
            description: UUID of the routine to delete
        responses:
          204:
            description: Routine deleted successfully (no content)
          401:
            description: Missing or invalid JWT token
          403:
            description: Forbidden – users with role "user" may not delete routines
          404:
            description: Routine not found
        """

    claims = get_jwt()
    if claims.get('role') == 'user':
        return {'error': 'Acesso negado'}, 403

    routine = get_routine(routine_id)
    delete_routine(routine)
    return '', 204

#--------------------- WEb ----------------------------
@routine_.route("/list_routines")
def list_routines_route():
    routines = list_routines()
    return render_template("routine.html", routines=routines)

@routine_.route('/register_routine', methods=['GET', 'POST'])
def register_routine():
    if request.method == 'POST':
        # Pega dados do formulário básico
        session['begin_time'] = request.form.get('begin_time')
        session['end_time'] = request.form.get('end_time')
        session['liters_of_water'] = request.form.get('liters_of_water')
        session['ativa'] = request.form.get('ativa')
        session['locale_id'] = request.form.get('locale_id')  # opcional se existir

        # Redireciona para a página de opções avançadas
        return redirect('/api/routine/opicoes_avancadas')
    locales = list_locales()
    return render_template('register_routine.html', locales= locales)

@routine_.route("/add_routine", methods=["POST"])
def add_routine():
    begin_time = request.form.get("begin_time")
    end_time = request.form.get("end_time")
    liters_of_water = request.form.get("liters_of_water")
    locale_id = request.form.get("locale_id")

    create_routine(
        begin_time=begin_time,
        end_time=end_time,
        liters_of_water=liters_of_water,
        locale_id=locale_id
    )

    return redirect("/api/routine/list_routines")

@routine_.route('/opicoes_avancadas', methods=['GET', 'POST'])
def opicoes_avancadas():
    if request.method == 'POST':
        # Dados do segundo formulário
        umidade_min = request.form.get('umidade_min')
        umidade_max = request.form.get('umidade_max')
        temperatura_min = request.form.get('temperatura_min')
        temperatura_max = request.form.get('temperatura_max')

        # Dados do primeiro formulário que estão na session
        begin_time = session.get('begin_time')
        end_time = session.get('end_time')
        liters_of_water = session.get('liters_of_water')
        ativa = session.get('ativa')
        locale_id = session.get('locale_id')

        # Aqui você faz a criação da rotina completa
        create_routine(
            temperature=temperatura_max,  # ou outro critério
            humidity=umidade_max,         # ou outro critério
            begin_time=begin_time,
            end_time=end_time,
            liters_of_water=liters_of_water,
            locale_id=locale_id
        )

        # Limpa a session depois de usar
        session.pop('begin_time', None)
        session.pop('end_time', None)
        session.pop('liters_of_water', None)
        session.pop('ativa', None)
        session.pop('locale_id', None)

        return redirect("/api/routine/list_routines")

    return render_template('opicoes_avancadas.html')

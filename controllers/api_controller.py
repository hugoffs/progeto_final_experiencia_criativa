# controllers/api_controller.py
from flask import Blueprint, jsonify
from models import Log

api_ = Blueprint('api', __name__)

@api_.route('/ultimo-log') # Note: agora é apenas '/ultimo-log'
def ultimo_log():
    log = Log.query.order_by(Log.created_at.desc()).first()
    if not log:
        return jsonify({'error': 'Nenhum dado encontrado'}), 404
    return jsonify(log.serialize()), 200
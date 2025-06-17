from flask import Blueprint, request, jsonify
import paho.mqtt.publish as publish

mqtt_ = Blueprint('mqtt', __name__)

@mqtt_.route('/mqtt/send', methods=['POST'])
def mqtt_send():
    data = request.get_json()
    valor = data.get('valor')

    if valor not in [0, 1]:
        return jsonify({'error': 'Valor deve ser 0 ou 1'}), 400

    try:
        publish.single(
            topic='mvp/atuador',
            payload=str(valor),
            hostname='broker.mqttdashboard.com'
        )
        return jsonify({'message': f'Valor {valor} enviado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

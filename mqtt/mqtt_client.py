#mqtt_client.py

from flask import Flask
from paho.mqtt import client as mqtt_client
import threading
import json
import time

from services.log_service import create_log
from models import db
from app import create_app  # ⚙️ Função que cria seu Flask app

# 🔗 Configurações MQTT
broker = 'broker.mqttdashboard.com'
port = 1883
topics = ['mvp/sensores']
client_id = f'flask-mqtt-listener-{int(time.time())}'

# ⚙️ Instancia o app Flask
flask_app, _ = create_app() # Use flask_app aqui

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('🟢 MQTT conectado')
        for topic in topics:
            client.subscribe(topic)
            print(f'📡 Inscrito em {topic}')
    else:
        print('🔴 Falha na conexão MQTT:', rc)

def on_message(client, userdata, msg):
    print(f'📥 Mensagem recebida {msg.topic}: {msg.payload.decode()}')

    try:
        data = json.loads(msg.payload.decode())

        required_fields = [
            'humidity', 'temperature', 'air_humidity', 'rain_status',
            'flow_rate', 'pulses', 'ldev_id'
        ]

        if not all(field in data for field in required_fields):
            print('⚠️ Dados incompletos recebidos')
            return

        humidity = float(data['humidity'])
        temperature = float(data['temperature'])
        air_humidity = float(data['air_humidity'])
        rain_status = str(data['rain_status'])
        flow_rate = float(data['flow_rate'])
        pulses = int(data['pulses'])
        is_irrigating = bool(data.get('is_irrigating', False))
        ldev_id = str(data['ldev_id'])

        # ⭐️ AQUI ESTÁ A CORREÇÃO: Use flask_app.app_context()
        with flask_app.app_context():
            create_log(
                humidity=humidity,
                temperature=temperature,
                air_humidity=air_humidity,
                rain_status=rain_status,
                flow_rate=flow_rate,
                pulses=pulses,
                is_irrigating=is_irrigating,
                ldev_id=ldev_id
            )
            print('✅ Log salvo no banco')

    except Exception as e:
        print('❌ Erro ao processar mensagem:', e)

def run_mqtt():
    client = mqtt_client.Client(client_id=client_id)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port)
    client.loop_forever()

# 🔥 Executa MQTT em uma thread paralela
mqtt_thread = threading.Thread(target=run_mqtt)
mqtt_thread.daemon = True
mqtt_thread.start()
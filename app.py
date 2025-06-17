from controllers.app_controller import create_app
from utils.create_db import create_database
from mqtt.mqtt_client import *

if __name__ == "__main__":
    app, socketio = create_app()
    #create_database(app)
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)

from controllers.app_controller import create_app
from utils.create_db import create_database 


if __name__ == "__main__":
    app = create_app()
    create_database(app)
    app.run(host='0.0.0.0', port=8080, debug=True)
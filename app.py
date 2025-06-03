from controllers.appcontroller import create_app
#from utils.create_db import create_database ##  conectar o banco de dados nesse ponto  


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)
from flask import Flask 
from models import *
from services.user_service import create_user


def create_database(app: Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_user("Usuário Admin", "admin@admin.net", "admin", role='admin')
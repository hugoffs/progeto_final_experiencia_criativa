from flask import Flask 
from models import *

def create_database(app: Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()
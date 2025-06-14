from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from models import db

class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.String(36), primary_key=True)
    humidity = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    is_irrigating = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    ldev_id = db.Column(db.String(36), db.ForeignKey('ldevs.id'), nullable=False)
    ldev = db.relationship('LDev', back_populates='logs')

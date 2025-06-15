from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from models import db

class Routine(db.Model):
    __tablename__ = 'routines'

    id = db.Column(db.String(36), primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    begin_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    liters_of_water = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    locale_id = db.Column(db.String(36), db.ForeignKey('locales.id'), nullable=False)
    locale = db.relationship('Locale', back_populates='routines')

    def serialize(self):
        return {
            'id': self.id,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'begin_time': self.begin_time.isoformat() if self.begin_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'liters_of_water': self.liters_of_water,
            'locale_id': self.locale_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

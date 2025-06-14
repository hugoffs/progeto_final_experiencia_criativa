from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from models import db

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    users = db.relationship('User', back_populates='team', lazy='dynamic')
    locales = db.relationship('Locale', back_populates='team', lazy='dynamic')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
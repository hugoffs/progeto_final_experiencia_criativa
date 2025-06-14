from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Locale(db.Model):
    __tablename__ = 'locales'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    note = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    team_id = db.Column(db.String(36), db.ForeignKey('teams.id'), nullable=False)
    team = db.relationship('Team', back_populates='locales')
    ldevs = db.relationship('LDev', back_populates='locale', lazy='dynamic')
    routines = db.relationship('Routine', back_populates='locale', lazy='dynamic')

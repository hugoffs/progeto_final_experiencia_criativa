from flask_sqlalchemy import SQLAlchemy

from models import db


class LDev(db.Model):
    __tablename__ = 'ldevs'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    latitude = db.Column(db.Numeric(10,8), nullable=False)
    longitude = db.Column(db.Numeric(10,8), nullable=False)

    locale_id = db.Column(db.String(36), db.ForeignKey('locales.id'), nullable=False)
    locale = db.relationship('Locale', back_populates='ldevs')
    logs = db.relationship('Log', back_populates='ldev', lazy='dynamic')
    errors = db.relationship('Error', back_populates='ldev', lazy='dynamic')

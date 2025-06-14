from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Error(db.Model):
    __tablename__ = 'errors'

    id = db.Column(db.String(36), primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    ldev_id = db.Column(db.String(36), db.ForeignKey('ldevs.id'), nullable=False)
    ldev = db.relationship('LDev', back_populates='errors')

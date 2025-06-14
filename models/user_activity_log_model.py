from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from models import db

class UserActivityLog(db.Model):
    __tablename__ = 'user_activity_logs'

    id = db.Column(db.String(36), primary_key=True)
    action = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='activity_logs')

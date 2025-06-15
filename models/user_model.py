from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from models import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column('password', db.String(255), nullable=False)
    role = db.Column(db.Enum('admin','operator','user'), nullable=False, default='user')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    team_id = db.Column(db.String(36), db.ForeignKey('teams.id'))
    team = db.relationship('Team', back_populates='users')
    activity_logs = db.relationship('UserActivityLog',
                                    back_populates='user',
                                    lazy='dynamic')

    # password property
    @property
    def password(self):
        raise AttributeError("Senha não pode ser lida.")

    @password.setter
    def password(self, plaintext):
        self.password_hash = generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return check_password_hash(self.password_hash, plaintext)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'team_id': self.team_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
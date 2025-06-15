from datetime import datetime

from models import db


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

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'note': self.note,
            'team_id': self.team_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

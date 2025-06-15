from models import db

class LDev(db.Model):
    __tablename__ = 'ldevs'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    latitude = db.Column(db.Numeric(9, 6), nullable=True)
    longitude = db.Column(db.Numeric(9, 6), nullable=True)

    locale_id = db.Column(db.String(36), db.ForeignKey('locales.id'), nullable=False)
    locale = db.relationship('Locale', back_populates='ldevs')
    logs = db.relationship('Log', back_populates='ldev', lazy='dynamic')
    errors = db.relationship('Error', back_populates='ldev', lazy='dynamic')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': float(self.latitude),
            'longitude': float(self.longitude),
            'locale_id': self.locale_id
        }

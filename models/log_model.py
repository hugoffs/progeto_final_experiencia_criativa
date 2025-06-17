# log_model.py

from datetime import datetime
from models import db

class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.String(36), primary_key=True)
    humidity = db.Column(db.Float, nullable=False)                  # Umidade do SOLO (%)
    temperature = db.Column(db.Float, nullable=False)               # Temperatura do AR (°C)
    air_humidity = db.Column(db.Float, nullable=False)              # Umidade do AR (%)
    rain_status = db.Column(db.String(10), nullable=False)          # "seco" ou "chovendo"
    flow_rate = db.Column(db.Float, nullable=False)                 # Vazão (litros/segundo)
    pulses = db.Column(db.Integer, nullable=False)                  # Pulsos brutos do sensor
    is_irrigating = db.Column(db.Boolean, nullable=False, default=False) # Atuador ligado?
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    ldev_id = db.Column(db.String(36), db.ForeignKey('ldevs.id'), nullable=False)
    ldev = db.relationship('LDev', back_populates='logs')

    def serialize(self):
        return {
            'id': self.id,
            'humidity': self.humidity,
            'temperature': self.temperature,
            'air_humidity': self.air_humidity,
            'rain_status': self.rain_status,
            'flow_rate': self.flow_rate,
            'pulses': self.pulses,
            'is_irrigating': self.is_irrigating,
            'created_at': self.created_at.isoformat(),
            'ldev_id': self.ldev_id
        }

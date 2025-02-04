# pago.py
from utils.db import db

class Pago(db.Model):
    __tablename__ = 'pago'

    id = db.Column(db.Integer, primary_key=True)
    metodo = db.Column(db.String(50), nullable=False)  # e.g., 'Tarjeta de Crédito', 'Efectivo'
    cantidad = db.Column(db.Float, nullable=False)
    referencia = db.Column(db.String(50), default="Sin Referencia") 

    # Foreign key linking to Orden
    id_orden = db.Column(db.Integer, db.ForeignKey('orden.id'), nullable=False)

    def __init__(self, metodo, cantidad, referencia, id_orden):
        self.metodo = metodo
        self.cantidad = cantidad
        self.referencia = referencia
        self.id_orden = id_orden

    def to_dict(self):
        return {
            'id': self.id,
            'metodo': self.metodo,
            'cantidad': self.cantidad,
            'referencia': self.referencia,
            'id_orden': self.id_orden
        }

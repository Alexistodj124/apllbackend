# pago.py
from utils.db import db

class Pago(db.Model):
    __tablename__ = 'pago'

    id = db.Column(db.Integer, primary_key=True)
    metodo = db.Column(db.String(50), nullable=False)  # e.g., 'Tarjeta de Crédito', 'Efectivo'
    cantidad = db.Column(db.Float, nullable=False)

    # Foreign key linking to Orden
    id_orden = db.Column(db.Integer, db.ForeignKey('orden.id'), nullable=False)

    def __init__(self, metodo, cantidad, id_orden):
        self.metodo = metodo
        self.cantidad = cantidad
        self.id_orden = id_orden

    def to_dict(self):
        return {
            'id': self.id,
            'metodo': self.metodo,
            'cantidad': self.cantidad,
            'id_orden': self.id_orden
        }

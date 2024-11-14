# orden.py
from datetime import datetime
from utils.db import db
from models.associations import orden_inventario  # Import the junction table

class Orden(db.Model):
    __tablename__ = 'orden'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.now)
    origen = db.Column(db.String(100), nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    bodeguero_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    total = db.Column(db.Float, nullable=False, default=0.0)

    # Relationships
    vendedor = db.relationship('Empleado', foreign_keys=[vendedor_id], backref='ventas')
    bodeguero = db.relationship('Empleado', foreign_keys=[bodeguero_id], backref='bodegas')
    pagos = db.relationship('Pago', backref='orden', cascade="all, delete-orphan")
    inventarios = db.relationship('Inventario', secondary=orden_inventario, backref='orders', overlaps="inventarios,ordenes")

    def __init__(self, origen, vendedor_id, bodeguero_id, total):
        self.origen = origen
        self.vendedor_id = vendedor_id
        self.bodeguero_id = bodeguero_id
        self.total = total

    def to_dict(self):
        return {
            'id': self.id,
            'fecha': self.fecha,
            'origen': self.origen,
            'total': self.total,
            'vendedor': self.vendedor.to_dict() if self.vendedor else None,
            'bodeguero': self.bodeguero.to_dict() if self.bodeguero else None,
            'pagos': [pago.to_dict() for pago in self.pagos],
            'inventarios': [inventario.to_dict() for inventario in self.inventarios]
        }

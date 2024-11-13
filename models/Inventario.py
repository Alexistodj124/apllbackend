# inventario.py
from utils.db import db
from models.associations import orden_inventario  # Import the junction table

class Inventario(db.Model):
    __tablename__ = 'inventario'

    id = db.Column(db.Integer, primary_key=True)
    id_carro = db.Column(db.Integer, db.ForeignKey('carro.id'), nullable=False)
    repuesto = db.Column(db.String(100), nullable=False)
    ingresados = db.Column(db.Integer, nullable=False)
    vendidos = db.Column(db.Integer, nullable=False, default=0)
    precio_unitario = db.Column(db.Float, nullable=False, default=0.0)

    # Relationships
    carro = db.relationship('Carro', backref='inventarios')
    inventarios = db.relationship('Inventario', secondary=orden_inventario, backref='ordenes')


    def __init__(self, id_carro, repuesto, ingresados, vendidos, precio_unitario):
        self.id_carro = id_carro
        self.repuesto = repuesto
        self.ingresados = ingresados
        self.vendidos = vendidos
        self.precio_unitario = precio_unitario

    @property
    def existencia(self):
        return self.ingresados - self.vendidos

    def to_dict(self):
        return {
            'id': self.id,
            'id_carro': self.id_carro,
            'repuesto': self.repuesto,
            'ingresados': self.ingresados,
            'vendidos': self.vendidos,
            'existencia': self.existencia,
            'precio_unitario': self.precio_unitario,
            'carro': self.carro.to_dict(),
            'ordenes': [orden.id for orden in self.ordenes]
        }
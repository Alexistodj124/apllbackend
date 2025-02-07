from utils.db import db
import base64

class Carro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100))
    linea = db.Column(db.String(100))
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'))  # Relación con Marca

    # Relación hacia el modelo Marca
    marca = db.relationship('Marca', backref='carros')

    def __init__(self, modelo, linea, marca_id):
        self.modelo = modelo
        self.linea = linea
        self.marca_id = marca_id

    def to_dict(self, include_logo=True):
        carro_data = {
            'id': self.id,
            'modelo': self.modelo,
            'linea': self.linea,
            'marca_id': self.marca_id,
            'marca': self.marca.to_dict(include_logo=include_logo) if self.marca else None
        }
        return carro_data

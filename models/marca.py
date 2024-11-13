import base64
from utils.db import db

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Marca = db.Column(db.String(100))
    Logo = db.Column(db.LargeBinary)  # Usamos LargeBinary para almacenar el logo en binario

    def __init__(self, Marca, Logo):
        self.Marca = Marca
        self.Logo = Logo

    def to_dict(self):
        return {
            'id': self.id,
            'Marca': self.Marca,
            'Logo': base64.b64encode(self.Logo).decode('utf-8') if self.Logo else None
        }

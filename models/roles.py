from utils.db import db

class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, rol):
        self.rol = rol

    def to_dict(self):
        return {
            'id': self.id,
            'rol': self.rol
        }

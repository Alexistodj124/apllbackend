from utils.db import db

class Empleado(db.Model):
    __tablename__ = 'empleado'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # Resolve conflicts by specifying overlaps
    usuario = db.relationship('Usuarios', backref='employee', uselist=False, overlaps="usuario.employee")

    def __init__(self, nombre, apellido, id_usuario):
        self.nombre = nombre
        self.apellido = apellido
        self.id_usuario = id_usuario

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'usuario': self.usuario.to_dict() if self.usuario else None
        }

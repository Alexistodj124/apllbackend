import bcrypt
from utils.db import db

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)  # Store hashed password
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    rol = db.relationship('Roles', backref='usuarios')
    empleado = db.relationship('Empleado', backref='user', uselist=False, overlaps="employee,usuario")

    def __init__(self, username, password, id_rol):
        self.username = username
        self.password = self.hash_password(password)  # Hash the password before storing
        self.id_rol = id_rol

    def hash_password(self, password):
        """Hashes the password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Checks if the provided password matches the hashed password."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'rol': self.rol.to_dict() if self.rol else None,
            'empleado': self.empleado.to_dict() if self.empleado else None
        }

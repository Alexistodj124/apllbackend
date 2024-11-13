from utils.db import db

# Junction table for many-to-many relationship between Orden and Inventario
orden_inventario = db.Table('orden_inventario',
    db.Column('orden_id', db.Integer, db.ForeignKey('orden.id'), primary_key=True),
    db.Column('inventario_id', db.Integer, db.ForeignKey('inventario.id'), primary_key=True)
)

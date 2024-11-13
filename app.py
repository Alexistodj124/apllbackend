from flask import Flask
from flask_migrate import Migrate
from utils.db import db
from config import DATABASE_CONNECTION_URI
from routes.carros import carros
from routes.roles import roles
from routes.bodega import bodegas
from routes.empleado import empleados
from routes.Inventario import inventarios
from routes.usuarios import usuarios
from routes.marca import marcas
from routes.orden import orden
from routes.pagos import pagos
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Inicializar la base de datos
db.init_app(app)

# Configurar Flask-Migrate
migrate = Migrate(app, db)

# Registrar los blueprints
app.register_blueprint(carros)
app.register_blueprint(roles)
app.register_blueprint(bodegas)
app.register_blueprint(usuarios)
app.register_blueprint(empleados)
app.register_blueprint(inventarios)
app.register_blueprint(marcas)
app.register_blueprint(orden)
app.register_blueprint(pagos)

if __name__ == '__main__':
    app.run(debug=True)
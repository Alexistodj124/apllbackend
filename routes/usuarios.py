from flask import Blueprint, request, jsonify
from models.usuarios import Usuarios
from utils.db import db

usuarios = Blueprint("usuarios", __name__)

# Get all users
@usuarios.route("/usuarios", methods=["GET"])
def get_usuarios():
    usuarios = Usuarios.query.all()
    if not usuarios:
        return jsonify({"mensaje": "No se encontraron usuarios"}), 404
    usuarios_list = [usuario.to_dict() for usuario in usuarios]
    return jsonify(usuarios_list), 200

# Get a specific user by ID
@usuarios.route("/usuarios/<int:id>", methods=["GET"])
def get_usuario(id):
    usuario = Usuarios.query.get(id)
    if usuario is None:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    return jsonify(usuario.to_dict()), 200

# Create a new user
@usuarios.route("/usuarios", methods=["POST"])
def crear_usuario():
    datos = request.get_json()
    username = datos.get("username")
    password = datos.get("password")
    id_rol = datos.get("id_rol")

    if not (username and password and id_rol):
        return jsonify({"mensaje": "Todos los campos son requeridos"}), 400

    # Check if username already exists
    if Usuarios.query.filter_by(username=username).first():
        return jsonify({"mensaje": "El nombre de usuario ya está en uso"}), 409

    new_usuario = Usuarios(username=username, password=password, id_rol=id_rol)
    db.session.add(new_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario guardado", "usuario": new_usuario.to_dict()}), 201

# Update an existing user
@usuarios.route("/usuarios/<int:id>", methods=["PUT"])
def actualizar_usuario(id):
    usuario = Usuarios.query.get(id)
    if usuario is None:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    datos = request.get_json()
    if not datos:
        return jsonify({"mensaje": "No se proporcionaron datos para actualizar"}), 400

    username = datos.get("username")
    password = datos.get("password")
    id_rol = datos.get("id_rol")

    if username:
        # Check if new username is unique
        if Usuarios.query.filter(Usuarios.username == username, Usuarios.id != id).first():
            return jsonify({"mensaje": "El nombre de usuario ya está en uso"}), 409
        usuario.username = username
    if password:
        usuario.password = password
    if id_rol:
        usuario.id_rol = id_rol

    db.session.commit()

    return jsonify({"mensaje": "Usuario actualizado", "usuario": usuario.to_dict()}), 200

# Delete a user by ID
@usuarios.route("/usuarios/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    usuario = Usuarios.query.get(id)
    if usuario is None:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario eliminado"}), 200


#LOGIN

@usuarios.route("/login", methods=["POST"])
def login():
    datos = request.get_json()
    username = datos.get("username")
    password = datos.get("password")

    # Find the user by username
    usuario = Usuarios.query.filter_by(username=username).first()
    if not usuario or not usuario.check_password(password):
        return jsonify({"mensaje": "Credenciales incorrectas"}), 401

    return jsonify({"mensaje": "Inicio de sesión exitoso", "usuario": usuario.to_dict()}), 200

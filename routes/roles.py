from flask import Blueprint, request, jsonify
from models.roles import Roles
from utils.db import db

roles = Blueprint("roles", __name__)

# Get all roles
@roles.route("/roles", methods=["GET"])
def get_roles():
    roles = Roles.query.all()
    if not roles:
        return jsonify({"mensaje": "No se encontraron roles"}), 404
    roles_list = [rol.to_dict() for rol in roles]
    return jsonify(roles_list), 200

# Get a specific role by ID
@roles.route("/roles/<int:id>", methods=["GET"])
def get_rol(id):
    rol = Roles.query.get(id)
    if rol is None:
        return jsonify({"mensaje": "Rol no encontrado"}), 404
    return jsonify(rol.to_dict()), 200

# Create a new role
@roles.route("/roles", methods=["POST"])
def crear_rol():
    datos = request.get_json()
    rol_name = datos.get("rol")

    if not rol_name:
        return jsonify({"mensaje": "El nombre del rol es requerido"}), 400

    # Check for uniqueness
    if Roles.query.filter_by(rol=rol_name).first():
        return jsonify({"mensaje": "El rol ya existe"}), 409

    new_rol = Roles(rol=rol_name)
    db.session.add(new_rol)
    db.session.commit()

    return jsonify({"mensaje": "Rol guardado", "rol": new_rol.to_dict()}), 201

# Update an existing role
@roles.route("/roles/<int:id>", methods=["PUT"])
def actualizar_rol(id):
    rol = Roles.query.get(id)
    if rol is None:
        return jsonify({"mensaje": "Rol no encontrado"}), 404

    datos = request.get_json()
    rol_info = datos.get("rol")

    if not rol_info:
        return jsonify({"mensaje": "No se proporcionaron datos para actualizar"}), 400

    rol.rol = rol_info
    db.session.commit()

    return jsonify({"mensaje": "Rol actualizado", "rol": rol.to_dict()}), 200

# Delete a role by ID
@roles.route("/roles/<int:id>", methods=["DELETE"])
def eliminar_rol(id):
    rol = Roles.query.get(id)
    if rol is None:
        return jsonify({"mensaje": "Rol no encontrado"}), 404

    db.session.delete(rol)
    db.session.commit()
    return jsonify({"mensaje": "Rol eliminado"}), 200

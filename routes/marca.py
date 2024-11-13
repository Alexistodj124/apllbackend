from flask import Blueprint, request, jsonify
from models.marca import Marca
from utils.db import db
import base64

marcas = Blueprint("marcas", __name__)

# Obtener todas las marcas
@marcas.route("/marcas", methods=["GET"])
def get_marcas():
    marcas = Marca.query.all()
    if not marcas:
        return jsonify({"mensaje": "No se encontraron marcas"}), 404
    marcas_list = [marca.to_dict() for marca in marcas]
    return jsonify(marcas_list), 200

# Obtener una marca por ID
@marcas.route("/marcas/<int:id>", methods=["GET"])
def get_marca(id):
    marca = Marca.query.get(id)
    if marca is None:
        return jsonify({"mensaje": "Marca no encontrada"}), 404
    return jsonify(marca.to_dict()), 200

# Crear una nueva marca
@marcas.route("/marcas", methods=["POST"])
def crear_marca():
    datos = request.form
    file = request.files.get('logo')

    if not file or file.filename == '':
        return jsonify({"mensaje": "No se proporcionó un logo"}), 400

    try:
        marca_nombre = datos.get("marca")
        if not marca_nombre:
            return jsonify({"mensaje": "El nombre de la marca es requerido"}), 400

        logo_binario = file.read()

        # Crear una nueva instancia de Marca
        new_marca = Marca(marca_nombre, logo_binario)
        db.session.add(new_marca)
        db.session.commit()

        return jsonify({"mensaje": "Marca guardada", "marca": new_marca.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": f"Error al guardar la marca: {str(e)}"}), 500

# Actualizar una marca por ID
@marcas.route("/marcas/<int:id>", methods=["PUT"])
def actualizar_marca(id):
    marca = Marca.query.get(id)
    if marca is None:
        return jsonify({"mensaje": "Marca no encontrada"}), 404

    datos = request.form or request.get_json()
    file = request.files.get('logo')

    marca_nombre = datos.get("marca")
    if marca_nombre:
        marca.Marca = marca_nombre

    if file and file.filename != '':
        logo_binario = file.read()
        marca.Logo = logo_binario

    db.session.commit()
    return jsonify({"mensaje": "Marca actualizada", "marca": marca.to_dict()}), 200

# Eliminar una marca por ID
@marcas.route("/marcas/<int:id>", methods=["DELETE"])
def eliminar_marca(id):
    marca = Marca.query.get(id)
    if marca is None:
        return jsonify({"mensaje": "Marca no encontrada"}), 404

    db.session.delete(marca)
    db.session.commit()
    return jsonify({"mensaje": "Marca eliminada"}), 200

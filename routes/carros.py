from flask import Blueprint, request, jsonify
from models.carro import Carro
from utils.db import db

carros = Blueprint("carros", __name__)


@carros.route("/carros", methods=["GET"])
def get_carros():
    carros = Carro.query.all()
    if not carros:
        return jsonify({"mensaje": "No se encontraron carros"}), 404
    carros_list = [carro.to_dict() for carro in carros]
    return jsonify(carros_list), 200


@carros.route("/carros/<int:id>", methods=["GET"])
def get_carro(id):
    carro = Carro.query.get(id)
    if carro is None:
        return jsonify({"mensaje": "Carro no encontrado"}), 404
    return jsonify(carro.to_dict()), 200

@carros.route("/carros/marca/<int:marca_id>", methods=["GET"])
def get_carros_by_marca(marca_id):
    carros = Carro.query.filter_by(marca_id=marca_id).all()
    if not carros:
        return jsonify({"mensaje": "No se encontraron carros para esta marca"}), 404
    carros_list = [carro.to_dict() for carro in carros]
    return jsonify(carros_list), 200


@carros.route("/carros", methods=["POST"])
def crear_carro():
    datos = request.get_json()

    modelo = datos.get("modelo")
    linea = datos.get("linea")
    marca_id = datos.get("marca_id")

    if not modelo or not linea or not marca_id:
        return jsonify({"mensaje": "Modelo, linea y marca_id son requeridos"}), 400

    new_carro = Carro(modelo=modelo, linea=linea, marca_id=marca_id)

    db.session.add(new_carro)
    db.session.commit()

    return jsonify({"mensaje": "Carro guardado", "carro": new_carro.to_dict()}), 201



@carros.route("/carros/<int:id>", methods=["PUT"])
def actualizar_carro(id):
    carro = Carro.query.get(id)
    if carro is None:
        return jsonify({"mensaje": "Carro no encontrado"}), 404

    datos = request.get_json()
    if not datos:
        return jsonify({"mensaje": "No se proporcionaron datos para actualizar"}), 400

    modelo = datos.get("modelo")
    linea = datos.get("linea")
    marca_id = datos.get("marca_id")

    if modelo:
        carro.modelo = modelo
    if linea:
        carro.linea = linea
    if marca_id:
        carro.marca_id = marca_id

    db.session.commit()

    return jsonify(carro.to_dict()), 200



@carros.route("/carros/<int:id>", methods=["DELETE"])
def eliminar_carro(id):
    carro = Carro.query.get(id)
    if carro is None:
        return jsonify({"mensaje": "Carro no encontrado"}), 404

    db.session.delete(carro)
    db.session.commit()
    return jsonify({"mensaje": "Carro eliminado"}), 200


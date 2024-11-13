# rutas/inventarios.py
from flask import Blueprint, request, jsonify
from models.Inventario import Inventario
from utils.db import db
from flask import session


inventarios = Blueprint("inventarios", __name__)

@inventarios.route("/inventarios", methods=["GET"])
def get_inventarios():
    inventarios = Inventario.query.all()
    if not inventarios:
        return jsonify({"mensaje": "No se encontraron inventarios"}), 404
    inventarios_list = [inventario.to_dict() for inventario in inventarios]
    return jsonify(inventarios_list), 200

@inventarios.route("/inventarios/<int:id>", methods=["GET"])
def get_inventario(id):
    inventario = Inventario.query.get(id)
    if inventario is None:
        return jsonify({"mensaje": "Inventario no encontrado"}), 404
    return jsonify(inventario.to_dict()), 200

@inventarios.route("/inventarios", methods=["POST"])
def crear_inventario():
    datos = request.get_json()
    id_carro = datos.get("id_carro")
    repuesto = datos.get("repuesto")
    ingresados = datos.get("ingresados")
    vendidos = datos.get("vendidos", 0)
    precio_unitario = datos.get("precio_unitario", 0.0)

    if not (id_carro and repuesto and ingresados is not None):
        return jsonify({"mensaje": "id_carro, repuesto, e ingresados son requeridos"}), 400

    new_inventario = Inventario(
        id_carro=id_carro,
        repuesto=repuesto,
        ingresados=ingresados,
        vendidos=vendidos,
        precio_unitario=precio_unitario
    )

    db.session.add(new_inventario)
    db.session.commit()

    return jsonify({"mensaje": "Inventario guardado", "inventario": new_inventario.to_dict()}), 201


@inventarios.route("/inventarios/<int:id>", methods=["PUT"])
def actualizar_inventario(id):
    inventario = Inventario.query.get(id)
    if inventario is None:
        return jsonify({"mensaje": "Inventario no encontrado"}), 404

    datos = request.get_json()
    if not datos:
        return jsonify({"mensaje": "No se proporcionaron datos para actualizar"}), 400

    id_carro = datos.get("id_carro")
    repuesto = datos.get("repuesto")
    ingresados = datos.get("ingresados")
    vendidos = datos.get("vendidos")
    precio_unitario = datos.get("precio_unitario")

    if id_carro is not None:
        inventario.id_carro = id_carro
    if repuesto is not None:
        inventario.repuesto = repuesto
    if ingresados is not None:
        inventario.ingresados = ingresados
    if vendidos is not None:
        inventario.vendidos = vendidos
    if precio_unitario is not None:
        inventario.precio_unitario = precio_unitario

    db.session.commit()

    return jsonify(inventario.to_dict()), 200


@inventarios.route("/inventarios/<int:id>", methods=["DELETE"])
def eliminar_inventario(id):
    inventario = Inventario.query.get(id)
    if inventario is None:
        return jsonify({"mensaje": "Inventario no encontrado"}), 404

    db.session.delete(inventario)
    db.session.commit()
    return jsonify({"mensaje": "Inventario eliminado"}), 200


# Agregar al carrito
def agregar_al_carrito(repuesto_id):
    if 'orden' not in session:
        session['carrito'] = []
    session['carrito'].append({'item_id': repuesto_id})

# Obtener el carrito
def obtener_carrito():
    return session.get('carrito', [])

# Limpiar el carrito después de hacer un pedido
def limpiar_carrito():
    session.pop('carrito', None)
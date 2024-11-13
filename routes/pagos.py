# pago_routes.py
from flask import Blueprint, request, jsonify
from utils.db import db
from models.pagos import Pago
from models.orden import Orden

pagos = Blueprint('pagos', __name__)

# Add a payment to an order
@pagos.route('/orden/<int:id_orden>/pago', methods=['POST'])
def add_pago(id_orden):
    data = request.json
    metodo = data.get('metodo')
    cantidad = data.get('cantidad')

    # Validation
    if not metodo or cantidad is None:
        return jsonify({'error': 'Metodo and cantidad are required'}), 400
    if not isinstance(cantidad, (int, float)) or cantidad <= 0:
        return jsonify({'error': 'Cantidad must be a positive number'}), 400

    # Ensure the order exists
    orden = Orden.query.get(id_orden)
    if not orden:
        return jsonify({'error': 'Orden not found'}), 404

    # Create and save the new payment
    nuevo_pago = Pago(metodo=metodo, cantidad=cantidad, id_orden=id_orden)
    db.session.add(nuevo_pago)
    db.session.commit()
    return jsonify(nuevo_pago.to_dict()), 201

# Get all payments for a specific order
@pagos.route('/orden/<int:id_orden>/pago', methods=['GET'])
def get_pagos_for_orden(id_orden):
    pagos = Pago.query.filter_by(id_orden=id_orden).all()
    if not pagos:
        return jsonify({'message': 'No payments found for this order'}), 404
    return jsonify([pago.to_dict() for pago in pagos]), 200

# Get a single payment by ID
@pagos.route('/pago/<int:id>', methods=['GET'])
def get_pago(id):
    pago = Pago.query.get(id)
    if pago:
        return jsonify(pago.to_dict()), 200
    return jsonify({'error': 'Pago not found'}), 404

# Update a payment by ID
@pagos.route('/pago/<int:id>', methods=['PUT'])
def update_pago(id):
    data = request.json
    pago = Pago.query.get(id)
    if not pago:
        return jsonify({'error': 'Pago not found'}), 404

    metodo = data.get('metodo')
    cantidad = data.get('cantidad')
    
    if metodo:
        pago.metodo = metodo
    if cantidad is not None:
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            return jsonify({'error': 'Cantidad must be a positive number'}), 400
        pago.cantidad = cantidad

    db.session.commit()
    return jsonify(pago.to_dict()), 200

# Delete a payment by ID
@pagos.route('/pago/<int:id>', methods=['DELETE'])
def delete_pago(id):
    pago = Pago.query.get(id)
    if pago:
        db.session.delete(pago)
        db.session.commit()
        return jsonify({'message': 'Pago deleted successfully'}), 200
    return jsonify({'error': 'Pago not found'}), 404

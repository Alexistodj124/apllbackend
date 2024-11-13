# orden_routes.py
from flask import Blueprint, request, jsonify
from utils.db import db
from models.orden import Orden
from models.empleado import Empleado
from models.Inventario import Inventario
from models.pagos import Pago

orden_bp = Blueprint('orden', __name__)

# Create a new order
@orden_bp.route('/orden', methods=['POST'])
def create_orden():
    data = request.json
    origen = data.get('origen')
    total = data.get('total', 0.0)
    vendedor_id = data.get('vendedor_id')
    bodeguero_id = data.get('bodeguero_id')
    inventarios_ids = data.get('inventarios', [])

    # Validation for required fields
    if not origen or not vendedor_id or not bodeguero_id:
        return jsonify({"error": "origen, vendedor_id, and bodeguero_id are required"}), 400

    # Validate vendedor and bodeguero existence
    vendedor = Empleado.query.get(vendedor_id)
    bodeguero = Empleado.query.get(bodeguero_id)
    if not vendedor or not bodeguero:
        return jsonify({"error": "Invalid vendedor_id or bodeguero_id"}), 400

    # Create the order
    nueva_orden = Orden(origen=origen, vendedor_id=vendedor_id, bodeguero_id=bodeguero_id, total=total)

    # Add Inventarios if provided
    for inventario_id in inventarios_ids:
        inventario = Inventario.query.get(inventario_id)
        if inventario:
            nueva_orden.inventarios.append(inventario)

    db.session.add(nueva_orden)
    db.session.commit()

    return jsonify(nueva_orden.to_dict()), 201

# Get all orders
@orden_bp.route('/orden', methods=['GET'])
def get_ordenes():
    ordenes = Orden.query.all()
    return jsonify([orden.to_dict() for orden in ordenes]), 200

# Get a single order by ID
@orden_bp.route('/orden/<int:id>', methods=['GET'])
def get_orden(id):
    orden = Orden.query.get(id)
    if orden:
        return jsonify(orden.to_dict()), 200
    return jsonify({'error': 'Orden not found'}), 404

# Update an order by ID
@orden_bp.route('/orden/<int:id>', methods=['PUT'])
def update_orden(id):
    data = request.json
    orden = Orden.query.get(id)
    if orden:
        orden.origen = data.get('origen', orden.origen)
        orden.total = data.get('total', orden.total)

        # Update vendedor_id and bodeguero_id
        vendedor_id = data.get('vendedor_id')
        bodeguero_id = data.get('bodeguero_id')
        if vendedor_id:
            vendedor = Empleado.query.get(vendedor_id)
            if vendedor:
                orden.vendedor_id = vendedor_id
            else:
                return jsonify({"error": "Invalid vendedor_id"}), 400
        if bodeguero_id:
            bodeguero = Empleado.query.get(bodeguero_id)
            if bodeguero:
                orden.bodeguero_id = bodeguero_id
            else:
                return jsonify({"error": "Invalid bodeguero_id"}), 400

        # Update associated Inventarios if provided
        inventarios_ids = data.get('inventarios', [])
        if inventarios_ids:
            orden.inventarios.clear()
            for inventario_id in inventarios_ids:
                inventario = Inventario.query.get(inventario_id)
                if inventario:
                    orden.inventarios.append(inventario)

        db.session.commit()
        return jsonify(orden.to_dict()), 200
    return jsonify({'error': 'Orden not found'}), 404

# Delete an order by ID
@orden_bp.route('/orden/<int:id>', methods=['DELETE'])
def delete_orden(id):
    orden = Orden.query.get(id)
    if orden:
        db.session.delete(orden)
        db.session.commit()
        return jsonify({'message': 'Orden deleted successfully'}), 200
    return jsonify({'error': 'Orden not found'}), 404

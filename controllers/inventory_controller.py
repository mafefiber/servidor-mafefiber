from flask import request, jsonify
from models import db, Inventory

def inventory_to_dict(inventory):
    return {
        'id': inventory.id,
        'product_id': inventory.product_id,
        'warehouse': inventory.warehouse,
        'quantity': inventory.quantity,
        'is_active': inventory.is_active,
        'updated_at': inventory.updated_at.isoformat() if inventory.updated_at else None
    }

def create_inventory():
    data = request.get_json()
    product_id = data.get('product_id')
    warehouse = data.get('warehouse')
    quantity = data.get('quantity', 0)
    if not product_id or not warehouse:
        return jsonify({'error': 'product_id y warehouse son requeridos'}), 400
    inventory = Inventory(
        product_id=product_id,
        warehouse=warehouse,
        quantity=quantity
    )
    db.session.add(inventory)
    db.session.commit()
    return jsonify(inventory_to_dict(inventory)), 201

def get_inventories():
    inventories = Inventory.query.filter_by(is_active=True).all()
    return jsonify([inventory_to_dict(i) for i in inventories]), 200

def get_inventory(inventory_id):
    inventory = Inventory.query.get_or_404(inventory_id)
    if not inventory.is_active:
        return jsonify({'error': 'Inventario no encontrado'}), 404
    return jsonify(inventory_to_dict(inventory)), 200

def update_inventory(inventory_id):
    inventory = Inventory.query.get_or_404(inventory_id)
    data = request.get_json()
    inventory.quantity = data.get('quantity', inventory.quantity)
    inventory.warehouse = data.get('warehouse', inventory.warehouse)
    db.session.commit()
    return jsonify(inventory_to_dict(inventory)), 200

def delete_inventory(inventory_id):
    inventory = Inventory.query.get_or_404(inventory_id)
    inventory.is_active = False
    db.session.commit()
    return jsonify({'message': 'Inventario desactivado'}), 200
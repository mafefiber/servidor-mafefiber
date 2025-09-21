from flask import request, jsonify
from models import db, CustomerType
# Convertir un objeto CustomerType a un diccionario
def customer_type_to_dict(customer_type):
    return {
        'id': customer_type.id,
        'name': customer_type.name,
        'description': customer_type.description,
        'is_active': customer_type.is_active,
        'create_at': customer_type.create_at.isoformat() if customer_type.create_at else None
    }

# Obtener todos los tipos de clientes
def get_customer_types():
    customer_types = CustomerType.query.filter_by(is_active=True).all()
    return jsonify([customer_type_to_dict(ct) for ct in customer_types]), 200

# Crear un nuevo tipo de cliente
def create_customer_type():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'error': 'El campo "name" es obligatorio'}), 400

    if CustomerType.query.filter_by(name=name).first():
        return jsonify({'error': 'El tipo de cliente ya existe'}), 400

    customer_type = CustomerType(
        name=name.strip(),
        description=description.strip() if description else None,
        is_active=True
    )
    db.session.add(customer_type)
    db.session.commit()
    return jsonify(customer_type_to_dict(customer_type)), 201

# Actualizar un tipo de cliente
def update_customer_type(customer_type_id):
    customer_type = CustomerType.query.get_or_404(customer_type_id)
    data = request.get_json()

    customer_type.name = data.get('name', customer_type.name).strip()
    customer_type.description = data.get('description', customer_type.description).strip()
    customer_type.is_active = data.get('is_active', customer_type.is_active)

    db.session.commit()
    return jsonify(customer_type_to_dict(customer_type)), 200

# Eliminar (desactivar) un tipo de cliente
def delete_customer_type(customer_type_id):
    customer_type = CustomerType.query.get_or_404(customer_type_id)
    customer_type.is_active = False
    db.session.commit()
    return jsonify({'message': 'Tipo de cliente desactivado'}), 200
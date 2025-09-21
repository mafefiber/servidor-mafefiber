from flask import request, jsonify
from models import db, Customer

def customer_to_dict(customer):
    return {
        'id': customer.id,
        'customer_type_id': customer.customer_type_id,
        'is_active': customer.is_active,
        'create_at': customer.create_at.isoformat() if customer.create_at else None
    }

def create_customer():
    data = request.get_json()
    customer_type_id = data.get('customer_type_id')
    if not customer_type_id:
        return jsonify({'error': 'customer_type_id requerido'}), 400
    customer = Customer(customer_type_id=customer_type_id)
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer_to_dict(customer)), 201

def get_customers():
    customers = Customer.query.filter_by(is_active=True).all()
    return jsonify([customer_to_dict(c) for c in customers]), 200

def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if not customer.is_active:
        return jsonify({'error': 'Cliente no encontrado'}), 404
    return jsonify(customer_to_dict(customer)), 200

def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()
    customer.customer_type_id = data.get('customer_type_id', customer.customer_type_id)
    db.session.commit()
    return jsonify(customer_to_dict(customer)), 200

def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer.is_active = False
    db.session.commit()
    return jsonify({'message': 'Cliente desactivado'}), 200
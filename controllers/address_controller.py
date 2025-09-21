from flask import request, jsonify
from models import db, Address
def address_to_dict(address):
    return {
        'id': address.id,
        'customer_id': address.customer_id,
        'address_line': address.address_line,
        'city': address.city,
        'state': address.state,
        'postal_code': address.postal_code,
        'country': address.country,
        'reference': address.reference,
        'is_default': address.is_default,
        'is_active': address.is_active,
        'created_at': address.created_at.isoformat() if address.created_at else None
    }

def create_address():
    data = request.get_json()
    customer_id = data.get('customer_id')
    address_line = data.get('address_line')
    city = data.get('city')
    country = data.get('country')
    if not customer_id or not address_line or not city or not country:
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    address = Address(
        customer_id=customer_id,
        address_line=address_line,
        city=city,
        state=data.get('state'),
        postal_code=data.get('postal_code'),
        country=country,
        reference=data.get('reference'),
        is_default=data.get('is_default', False)
    )
    db.session.add(address)
    db.session.commit()
    return jsonify(address_to_dict(address)), 201

def get_addresses():
    addresses = Address.query.filter_by(is_active=True).all()
    return jsonify([address_to_dict(a) for a in addresses]), 200

def get_address(address_id):
    address = Address.query.get_or_404(address_id)
    if not address.is_active:
        return jsonify({'error': 'Dirección no encontrada'}), 404
    return jsonify(address_to_dict(address)), 200

def update_address(address_id):
    address = Address.query.get_or_404(address_id)
    data = request.get_json()
    address.address_line = data.get('address_line', address.address_line)
    address.city = data.get('city', address.city)
    address.state = data.get('state', address.state)
    address.postal_code = data.get('postal_code', address.postal_code)
    address.country = data.get('country', address.country)
    address.reference = data.get('reference', address.reference)
    address.is_default = data.get('is_default', address.is_default)
    db.session.commit()
    return jsonify(address_to_dict(address)), 200

def delete_address(address_id):
    address = Address.query.get_or_404(address_id)
    address.is_active = False
    db.session.commit()
    return jsonify({'message': 'Dirección desactivada'}), 200
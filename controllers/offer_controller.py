from flask import request, jsonify
from models import db, Offer

def offer_to_dict(offer):
    return {
        'id': offer.id,
        'title': offer.title,
        'description': offer.description,
        'start_date': offer.start_date.isoformat() if offer.start_date else None,
        'end_date': offer.end_date.isoformat() if offer.end_date else None,
        'discount_type': offer.discount_type,
        'discount_value': float(offer.discount_value),
        'is_active': offer.is_active,
        'created_at': offer.created_at.isoformat() if offer.created_at else None
    }

def create_offer():
    data = request.get_json()
    title = data.get('title')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    discount_type = data.get('discount_type')
    discount_value = data.get('discount_value')
    if not title or not start_date or not end_date or not discount_type or not discount_value:
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    offer = Offer(
        title=title,
        description=data.get('description'),
        start_date=start_date,
        end_date=end_date,
        discount_type=discount_type,
        discount_value=discount_value
    )
    db.session.add(offer)
    db.session.commit()
    return jsonify(offer_to_dict(offer)), 201

def get_offers():
    offers = Offer.query.filter_by(is_active=True).all()
    return jsonify([offer_to_dict(o) for o in offers]), 200

def get_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    if not offer.is_active:
        return jsonify({'error': 'Oferta no encontrada'}), 404
    return jsonify(offer_to_dict(offer)), 200

def update_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    data = request.get_json()
    offer.title = data.get('title', offer.title)
    offer.description = data.get('description', offer.description)
    offer.start_date = data.get('start_date', offer.start_date)
    offer.end_date = data.get('end_date', offer.end_date)
    offer.discount_type = data.get('discount_type', offer.discount_type)
    offer.discount_value = data.get('discount_value', offer.discount_value)
    db.session.commit()
    return jsonify(offer_to_dict(offer)), 200

def delete_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    offer.is_active = False
    db.session.commit()
    return jsonify({'message': 'Oferta desactivada'}), 200
from flask import request, jsonify
from models import db, Coupon, OrderCoupon

def coupon_to_dict(coupon):
    return {
        'id': coupon.id,
        'code': coupon.code,
        'description': coupon.description,
        'discount_type': coupon.discount_type,
        'discount_value': float(coupon.discount_value),
        'valid_from': coupon.valid_from.isoformat() if coupon.valid_from else None,
        'valid_to': coupon.valid_to.isoformat() if coupon.valid_to else None,
        'usage_limit': coupon.usage_limit,
        'used_count': coupon.used_count,
        'is_active': coupon.is_active,
        'created_at': coupon.created_at.isoformat() if coupon.created_at else None
    }

def create_coupon():
    data = request.get_json()
    code = data.get('code')
    discount_type = data.get('discount_type')
    discount_value = data.get('discount_value')
    if not code or not discount_type or not discount_value:
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    coupon = Coupon(
        code=code,
        description=data.get('description'),
        discount_type=discount_type,
        discount_value=discount_value,
        valid_from=data.get('valid_from'),
        valid_to=data.get('valid_to'),
        usage_limit=data.get('usage_limit'),
        used_count=data.get('used_count', 0)
    )
    db.session.add(coupon)
    db.session.commit()
    return jsonify(coupon_to_dict(coupon)), 201

def get_coupons():
    coupons = Coupon.query.filter_by(is_active=True).all()
    return jsonify([coupon_to_dict(c) for c in coupons]), 200

def get_coupon(coupon_id):
    coupon = Coupon.query.get_or_404(coupon_id)
    if not coupon.is_active:
        return jsonify({'error': 'Cupón no encontrado'}), 404
    return jsonify(coupon_to_dict(coupon)), 200

def update_coupon(coupon_id):
    coupon = Coupon.query.get_or_404(coupon_id)
    data = request.get_json()
    coupon.code = data.get('code', coupon.code)
    coupon.description = data.get('description', coupon.description)
    coupon.discount_type = data.get('discount_type', coupon.discount_type)
    coupon.discount_value = data.get('discount_value', coupon.discount_value)
    coupon.valid_from = data.get('valid_from', coupon.valid_from)
    coupon.valid_to = data.get('valid_to', coupon.valid_to)
    coupon.usage_limit = data.get('usage_limit', coupon.usage_limit)
    coupon.used_count = data.get('used_count', coupon.used_count)
    db.session.commit()
    return jsonify(coupon_to_dict(coupon)), 200

def delete_coupon(coupon_id):
    coupon = Coupon.query.get_or_404(coupon_id)
    coupon.is_active = False
    db.session.commit()
    return jsonify({'message': 'Cupón desactivado'}), 200

def apply_coupon():
    data = request.get_json()
    order_id = data.get('order_id')
    coupon_id = data.get('coupon_id')
    discount_amount = data.get('discount_amount')
    if not order_id or not coupon_id or not discount_amount:
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    order_coupon = OrderCoupon(
        order_id=order_id,
        coupon_id=coupon_id,
        discount_amount=discount_amount
    )
    db.session.add(order_coupon)
    db.session.commit()
    return jsonify({
        'id': order_coupon.id,
        'order_id': order_coupon.order_id,
        'coupon_id': order_coupon.coupon_id,
        'discount_amount': float(order_coupon.discount_amount),
        'applied_at': order_coupon.applied_at.isoformat() if order_coupon.applied_at else None,
        'is_active': order_coupon.is_active
    }), 201
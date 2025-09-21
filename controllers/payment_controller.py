from flask import request, jsonify
from models import db, Payment

def payment_to_dict(payment):
    return {
        'id': payment.id,
        'order_id': payment.order_id,
        'subscription_id': payment.subscription_id,
        'customer_id': payment.customer_id,
        'amount': float(payment.amount),
        'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
        'payment_method': payment.payment_method,
        'reference': payment.reference,
        'status': payment.status,
        'is_active': payment.is_active,
        'created_at': payment.created_at.isoformat() if payment.created_at else None
    }

def create_payment():
    data = request.get_json()
    order_id = data.get('order_id')
    customer_id = data.get('customer_id')
    amount = data.get('amount')
    payment_method = data.get('payment_method')
    status = data.get('status', 'pending')
    if not order_id or not customer_id or not amount or not payment_method:
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    payment = Payment(
        order_id=order_id,
        subscription_id=data.get('subscription_id'),
        customer_id=customer_id,
        amount=amount,
        payment_method=payment_method,
        reference=data.get('reference'),
        status=status
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify(payment_to_dict(payment)), 201

def get_payments():
    payments = Payment.query.filter_by(is_active=True).all()
    return jsonify([payment_to_dict(p) for p in payments]), 200

def get_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    if not payment.is_active:
        return jsonify({'error': 'Pago no encontrado'}), 404
    return jsonify(payment_to_dict(payment)), 200

def update_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    data = request.get_json()
    payment.amount = data.get('amount', payment.amount)
    payment.payment_method = data.get('payment_method', payment.payment_method)
    payment.reference = data.get('reference', payment.reference)
    payment.status = data.get('status', payment.status)
    db.session.commit()
    return jsonify(payment_to_dict(payment)), 200

def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    payment.is_active = False
    db.session.commit()
    return jsonify({'message': 'Pago desactivado'}), 200
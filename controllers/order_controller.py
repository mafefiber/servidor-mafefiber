from flask import request, jsonify
from models import db, Order, OrderItem, Product

def order_to_dict(order):
    return {
        'id': order.id,
        'customer_id': order.customer_id,
        'user_id': order.user_id,
        'total_amount': float(order.total_amount),
        'status': order.status,
        'payment_method': order.payment_method,
        'is_active': order.is_active,
        'created_at': order.created_at.isoformat() if order.created_at else None,
        'items': [
            {
                'id': item.id,
                'product_id': item.product_id,
                'plan_id': item.plan_id,
                'quantity': item.quantity,
                'unit_price': float(item.unit_price)
            } for item in order.items
        ]
    }

def create_order():
    data = request.get_json()
    customer_id = data.get('customer_id')
    user_id = data.get('user_id')
    status = data.get('status', 'pending')
    payment_method = data.get('payment_method')
    items = data.get('items', [])

    if not customer_id or not items:
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    total_amount = 0
    order_items = []
    for item in items:
        product_id = item.get('product_id')
        plan_id = item.get('plan_id')
        quantity = item.get('quantity', 1)
        unit_price = item.get('unit_price')
        if not unit_price:
            # Si no se envía el precio, lo toma del producto
            if product_id:
                product = Product.query.get(product_id)
                if not product:
                    return jsonify({'error': f'Producto {product_id} no existe'}), 400
                unit_price = float(product.price)
            else:
                return jsonify({'error': 'unit_price requerido si no hay product_id'}), 400
        total_amount += float(unit_price) * quantity
        order_items.append(OrderItem(
            product_id=product_id,
            plan_id=plan_id,
            quantity=quantity,
            unit_price=unit_price
        ))

    order = Order(
        customer_id=customer_id,
        user_id=user_id,
        total_amount=total_amount,
        status=status,
        payment_method=payment_method
    )
    db.session.add(order)
    db.session.flush()  # Para obtener el id del pedido antes de agregar los items

    for item in order_items:
        item.order_id = order.id
        db.session.add(item)

    db.session.commit()
    return jsonify(order_to_dict(order)), 201

def get_orders():
    orders = Order.query.filter_by(is_active=True).all()
    return jsonify([order_to_dict(o) for o in orders]), 200

def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    if not order.is_active:
        return jsonify({'error': 'Pedido no encontrado'}), 404
    return jsonify(order_to_dict(order)), 200

def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    order.status = data.get('status', order.status)
    order.payment_method = data.get('payment_method', order.payment_method)
    db.session.commit()
    return jsonify(order_to_dict(order)), 200

def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.is_active = False
    db.session.commit()
    return jsonify({'message': 'Pedido desactivado'}), 200
from flask import request, jsonify
from models import db, Comment
def comment_to_dict(comment):
    return {
        'id': comment.id,
        'customer_id': comment.customer_id,
        'subscription_id': comment.subscription_id,
        'product_id': comment.product_id,
        'plan_id': comment.plan_id,
        'service_request_id': comment.service_request_id,
        'user_id': comment.user_id,
        'content': comment.content,
        'rating': comment.rating,
        'is_active': comment.is_active,
        'created_at': comment.created_at.isoformat() if comment.created_at else None
    }

def create_comment():
    data = request.get_json()
    user_id = data.get('user_id')
    content = data.get('content')
    if not user_id or not content:
        return jsonify({'error': 'user_id y content son requeridos'}), 400
    comment = Comment(
        customer_id=data.get('customer_id'),
        subscription_id=data.get('subscription_id'),
        product_id=data.get('product_id'),
        plan_id=data.get('plan_id'),
        service_request_id=data.get('service_request_id'),
        user_id=user_id,
        content=content,
        rating=data.get('rating')
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment_to_dict(comment)), 201

def get_comments():
    comments = Comment.query.filter_by(is_active=True).all()
    return jsonify([comment_to_dict(c) for c in comments]), 200

def get_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.is_active:
        return jsonify({'error': 'Comentario no encontrado'}), 404
    return jsonify(comment_to_dict(comment)), 200

def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json()
    comment.content = data.get('content', comment.content)
    comment.rating = data.get('rating', comment.rating)
    db.session.commit()
    return jsonify(comment_to_dict(comment)), 200

def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.is_active = False
    db.session.commit()
    return jsonify({'message': 'Comentario desactivado'}), 200
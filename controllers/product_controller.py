from flask import request, jsonify
from models import db, Product

def product_to_dict(product):
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float(product.price),
        'sku': product.sku,
        'stock_quantity': product.stock_quantity,
        'images': product.images.split('\n') if product.images else [],
        'is_active': product.is_active,
        'created_at': product.create_at.isoformat() if product.create_at else None
    }

def create_product():
    """
    Crear un nuevo producto
    """
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    sku = data.get('sku')
    stock_quantity = data.get('stock_quantity', 0)
    images = data.get('images', [])

    if not name or not price or not sku:
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    product = Product(
        name=name,
        description=description,
        price=price,
        sku=sku,
        stock_quantity=stock_quantity,
        images='\n'.join(images) if images else None
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product_to_dict(product)), 201

def get_products():
    """
    Obtener lista de todos los productos activos
    """
    products = Product.query.filter_by(is_active=True).all()
    return jsonify([product_to_dict(p) for p in products]), 200

def get_product(product_id):
    """
    Obtener un producto específico por ID
    """
    product = Product.query.get_or_404(product_id)
    if not product.is_active:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify(product_to_dict(product)), 200

def update_product(product_id):
    """
    Actualizar un producto existente
    """
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.sku = data.get('sku', product.sku)
    product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
    images = data.get('images')
    if images is not None:
        product.images = '\n'.join(images)
    db.session.commit()
    return jsonify(product_to_dict(product)), 200

def delete_product(product_id):
    """
    Desactivar un producto (soft delete)
    """
    product = Product.query.get_or_404(product_id)
    product.is_active = False
    db.session.commit()
    return jsonify({'message': 'Producto desactivado'}), 200
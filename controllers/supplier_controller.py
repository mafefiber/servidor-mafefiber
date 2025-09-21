from flask import request, jsonify
from models import db, Supplier, ProductPurchase

def supplier_to_dict(supplier):
    return {
        'id': supplier.id,
        'name': supplier.name,
        'contact_name': supplier.contact_name,
        'contact_email': supplier.contact_email,
        'contact_phone': supplier.contact_phone,
        'address': supplier.address,
        'tax_id': supplier.tax_id,
        'is_active': supplier.is_active,
        'created_at': supplier.created_at.isoformat() if supplier.created_at else None
    }

def create_supplier():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'name es requerido'}), 400
    supplier = Supplier(
        name=name,
        contact_name=data.get('contact_name'),
        contact_email=data.get('contact_email'),
        contact_phone=data.get('contact_phone'),
        address=data.get('address'),
        tax_id=data.get('tax_id')
    )
    db.session.add(supplier)
    db.session.commit()
    return jsonify(supplier_to_dict(supplier)), 201

def get_suppliers():
    suppliers = Supplier.query.filter_by(is_active=True).all()
    return jsonify([supplier_to_dict(s) for s in suppliers]), 200

def get_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    if not supplier.is_active:
        return jsonify({'error': 'Proveedor no encontrado'}), 404
    return jsonify(supplier_to_dict(supplier)), 200

def update_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    data = request.get_json()
    supplier.name = data.get('name', supplier.name)
    supplier.contact_name = data.get('contact_name', supplier.contact_name)
    supplier.contact_email = data.get('contact_email', supplier.contact_email)
    supplier.contact_phone = data.get('contact_phone', supplier.contact_phone)
    supplier.address = data.get('address', supplier.address)
    supplier.tax_id = data.get('tax_id', supplier.tax_id)
    db.session.commit()
    return jsonify(supplier_to_dict(supplier)), 200

def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    supplier.is_active = False
    db.session.commit()
    return jsonify({'message': 'Proveedor desactivado'}), 200

def purchase_to_dict(purchase):
    return {
        'id': purchase.id,
        'supplier_id': purchase.supplier_id,
        'product_id': purchase.product_id,
        'quantity': purchase.quantity,
        'unit_price': float(purchase.unit_price),
        'total_price': float(purchase.total_price),
        'purchase_date': purchase.purchase_date.isoformat() if purchase.purchase_date else None,
        'invoice_number': purchase.invoice_number,
        'is_active': purchase.is_active,
        'created_at': purchase.created_at.isoformat() if purchase.created_at else None
    }

def create_product_purchase():
    data = request.get_json()
    supplier_id = data.get('supplier_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    unit_price = data.get('unit_price')
    total_price = data.get('total_price')
    if not supplier_id or not product_id or not quantity or not unit_price or not total_price:
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    purchase = ProductPurchase(
        supplier_id=supplier_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
        total_price=total_price,
        invoice_number=data.get('invoice_number')
    )
    db.session.add(purchase)
    db.session.commit()
    return jsonify(purchase_to_dict(purchase)), 201

def get_product_purchases():
    purchases = ProductPurchase.query.filter_by(is_active=True).all()
    return jsonify([purchase_to_dict(p) for p in purchases]), 200

def get_product_purchase(purchase_id):
    purchase = ProductPurchase.query.get_or_404(purchase_id)
    if not purchase.is_active:
        return jsonify({'error': 'Compra no encontrada'}), 404
    return jsonify(purchase_to_dict(purchase)), 200

def update_product_purchase(purchase_id):
    purchase = ProductPurchase.query.get_or_404(purchase_id)
    data = request.get_json()
    purchase.quantity = data.get('quantity', purchase.quantity)
    purchase.unit_price = data.get('unit_price', purchase.unit_price)
    purchase.total_price = data.get('total_price', purchase.total_price)
    purchase.invoice_number = data.get('invoice_number', purchase.invoice_number)
    db.session.commit()
    return jsonify(purchase_to_dict(purchase)), 200

def delete_product_purchase(purchase_id):
    purchase = ProductPurchase.query.get_or_404(purchase_id)
    purchase.is_active = False
    db.session.commit()
    return jsonify({'message': 'Compra desactivada'}), 200
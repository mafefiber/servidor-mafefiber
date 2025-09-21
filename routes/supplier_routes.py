from flask import Blueprint
from controllers.supplier_controller import (
    create_supplier, get_suppliers, get_supplier, update_supplier, delete_supplier,
    create_product_purchase, get_product_purchases, get_product_purchase, update_product_purchase, delete_product_purchase
)

supplier_bp = Blueprint('supplier_bp', __name__)

# Proveedores
supplier_bp.route('/suppliers', methods=['POST'])(create_supplier)
supplier_bp.route('/suppliers', methods=['GET'])(get_suppliers)
supplier_bp.route('/suppliers/<int:supplier_id>', methods=['GET'])(get_supplier)
supplier_bp.route('/suppliers/<int:supplier_id>', methods=['PUT'])(update_supplier)
supplier_bp.route('/suppliers/<int:supplier_id>', methods=['DELETE'])(delete_supplier)

# Compras de productos
supplier_bp.route('/product-purchases', methods=['POST'])(create_product_purchase)
supplier_bp.route('/product-purchases', methods=['GET'])(get_product_purchases)
supplier_bp.route('/product-purchases/<int:purchase_id>', methods=['GET'])(get_product_purchase)
supplier_bp.route('/product-purchases/<int:purchase_id>', methods=['PUT'])(update_product_purchase)
supplier_bp.route('/product-purchases/<int:purchase_id>', methods=['DELETE'])(delete_product_purchase)
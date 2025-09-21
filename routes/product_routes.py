from flask import Blueprint
from controllers.product_controller import (
    create_product, get_products, get_product, update_product, delete_product
)

product_bp = Blueprint('product_bp', __name__)

product_bp.route('/products', methods=['POST'])(create_product)
product_bp.route('/products', methods=['GET'])(get_products)
product_bp.route('/products/<int:product_id>', methods=['GET'])(get_product)
product_bp.route('/products/<int:product_id>', methods=['PUT'])(update_product)
product_bp.route('/products/<int:product_id>', methods=['DELETE'])(delete_product)
from flask import Blueprint
from controllers.order_controller import (
    create_order, get_orders, get_order, update_order, delete_order
)

order_bp = Blueprint('order_bp', __name__)

order_bp.route('/orders', methods=['POST'])(create_order)
order_bp.route('/orders', methods=['GET'])(get_orders)
order_bp.route('/orders/<int:order_id>', methods=['GET'])(get_order)
order_bp.route('/orders/<int:order_id>', methods=['PUT'])(update_order)
order_bp.route('/orders/<int:order_id>', methods=['DELETE'])(delete_order)
from flask import Blueprint
from controllers.customer_controller import (
    create_customer, get_customers, get_customer, update_customer, delete_customer
)

customer_bp = Blueprint('customer_bp', __name__)

customer_bp.route('/customers', methods=['POST'])(create_customer)
customer_bp.route('/customers', methods=['GET'])(get_customers)
customer_bp.route('/customers/<int:customer_id>', methods=['GET'])(get_customer)
customer_bp.route('/customers/<int:customer_id>', methods=['PUT'])(update_customer)
customer_bp.route('/customers/<int:customer_id>', methods=['DELETE'])(delete_customer)
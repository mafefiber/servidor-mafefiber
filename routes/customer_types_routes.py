from flask import Blueprint
from controllers.customer_types_controller import (
    get_customer_types,
    create_customer_type,
    update_customer_type,
    delete_customer_type
)

customer_types_routes = Blueprint('customer_types_routes', __name__)

# Rutas para los tipos de clientes
customer_types_routes.route('/customer-types', methods=['GET'])(get_customer_types)
customer_types_routes.route('/customer-types', methods=['POST'])(create_customer_type)
customer_types_routes.route('/customer-types/<int:customer_type_id>', methods=['PUT'])(update_customer_type)
customer_types_routes.route('/customer-types/<int:customer_type_id>', methods=['DELETE'])(delete_customer_type)
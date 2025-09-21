from flask import Blueprint
from controllers.address_controller import (
    create_address, get_addresses, get_address, update_address, delete_address
)

address_bp = Blueprint('address_bp', __name__)

address_bp.route('/addresses', methods=['POST'])(create_address)
address_bp.route('/addresses', methods=['GET'])(get_addresses)
address_bp.route('/addresses/<int:address_id>', methods=['GET'])(get_address)
address_bp.route('/addresses/<int:address_id>', methods=['PUT'])(update_address)
address_bp.route('/addresses/<int:address_id>', methods=['DELETE'])(delete_address)
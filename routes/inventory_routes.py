from flask import Blueprint
from controllers.inventory_controller import (
    create_inventory, get_inventories, get_inventory, update_inventory, delete_inventory
)

inventory_bp = Blueprint('inventory_bp', __name__)

inventory_bp.route('/inventories', methods=['POST'])(create_inventory)
inventory_bp.route('/inventories', methods=['GET'])(get_inventories)
inventory_bp.route('/inventories/<int:inventory_id>', methods=['GET'])(get_inventory)
inventory_bp.route('/inventories/<int:inventory_id>', methods=['PUT'])(update_inventory)
inventory_bp.route('/inventories/<int:inventory_id>', methods=['DELETE'])(delete_inventory)
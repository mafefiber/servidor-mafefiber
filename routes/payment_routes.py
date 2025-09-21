from flask import Blueprint
from controllers.payment_controller import (
    create_payment, get_payments, get_payment, update_payment, delete_payment
)

payment_bp = Blueprint('payment_bp', __name__)

payment_bp.route('/payments', methods=['POST'])(create_payment)
payment_bp.route('/payments', methods=['GET'])(get_payments)
payment_bp.route('/payments/<int:payment_id>', methods=['GET'])(get_payment)
payment_bp.route('/payments/<int:payment_id>', methods=['PUT'])(update_payment)
payment_bp.route('/payments/<int:payment_id>', methods=['DELETE'])(delete_payment)
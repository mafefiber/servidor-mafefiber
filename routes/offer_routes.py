from flask import Blueprint
from controllers.offer_controller import (
    create_offer, get_offers, get_offer, update_offer, delete_offer
)

offer_bp = Blueprint('offer_bp', __name__)

offer_bp.route('/offers', methods=['POST'])(create_offer)
offer_bp.route('/offers', methods=['GET'])(get_offers)
offer_bp.route('/offers/<int:offer_id>', methods=['GET'])(get_offer)
offer_bp.route('/offers/<int:offer_id>', methods=['PUT'])(update_offer)
offer_bp.route('/offers/<int:offer_id>', methods=['DELETE'])(delete_offer)
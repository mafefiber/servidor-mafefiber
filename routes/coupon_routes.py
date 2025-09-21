from flask import Blueprint
from controllers.coupon_controller import (
    create_coupon, get_coupons, get_coupon, update_coupon, delete_coupon, apply_coupon
)

coupon_bp = Blueprint('coupon_bp', __name__)

coupon_bp.route('/coupons', methods=['POST'])(create_coupon)
coupon_bp.route('/coupons', methods=['GET'])(get_coupons)
coupon_bp.route('/coupons/<int:coupon_id>', methods=['GET'])(get_coupon)
coupon_bp.route('/coupons/<int:coupon_id>', methods=['PUT'])(update_coupon)
coupon_bp.route('/coupons/<int:coupon_id>', methods=['DELETE'])(delete_coupon)
coupon_bp.route('/order-coupons', methods=['POST'])(apply_coupon)
from flask import Blueprint
from controllers.plan_promotion_controller import (
    associate_promotion, list_promotions_by_plan, remove_plan_promotion
)

plan_promo_bp = Blueprint('plan_promo_bp', __name__)

plan_promo_bp.route('/plans/<int:plan_id>/promotions', methods=['POST'])(associate_promotion)
plan_promo_bp.route('/plans/<int:plan_id>/promotions', methods=['GET'])(list_promotions_by_plan)
plan_promo_bp.route('/plan-promotions/<int:pp_id>', methods=['DELETE'])(remove_plan_promotion)

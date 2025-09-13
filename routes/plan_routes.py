from flask import Blueprint
from controllers.plan_controller import (
    create_plan,get_plans,get_plan,update_plan,delete_plan
)

plan_bp=Blueprint('plan_bp',__name__)

plan_bp.route('/plans',methods=['POST'])(create_plan)
plan_bp.route('/plans',methods=['GET'])(get_plans)
plan_bp.route('/plans/<int:plan_id>',methods=['GET'])(get_plan)
plan_bp.route('/plans/<int:plan_id>',methods=['PUT'])(update_plan)
plan_bp.route('/plans/<int:plan_id>',methods=['DELETE'])(delete_plan)


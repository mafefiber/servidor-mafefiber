from flask import Blueprint
from controllers.plan_feature_controller import (
    create_feature,get_features_by_plan,update_feature,delete_feature
)

feature_bp = Blueprint('feature_bp',__name__)

feature_bp.route('/plans/<int:plan_id>/features',methods=['POST'])(create_feature)
feature_bp.route('/plans/<int:plan_id>/features',methods=['GET'])(get_features_by_plan)
feature_bp.route('/features/<int:feature_id>',methods=['PUT'])(update_feature)
feature_bp.route('/features/<int:feature_id>',methods=['DELETE'])(delete_feature)
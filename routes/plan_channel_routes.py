from flask import Blueprint
from controllers.plan_channel_controller import (
    associate_channel, list_channels_by_plan, remove_plan_channel
)

plan_channel_bp = Blueprint('plan_channel_bp', __name__)

plan_channel_bp.route('/plans/<int:plan_id>/channels', methods=['POST'])(associate_channel)
plan_channel_bp.route('/plans/<int:plan_id>/channels', methods=['GET'])(list_channels_by_plan)
plan_channel_bp.route('/plan-channels/<int:pc_id>', methods=['DELETE'])(remove_plan_channel)
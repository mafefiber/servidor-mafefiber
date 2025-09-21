from flask import Blueprint
from controllers.comment_controller import (
    create_comment, get_comments, get_comment, update_comment, delete_comment
)

comment_bp = Blueprint('comment_bp', __name__)

comment_bp.route('/comments', methods=['POST'])(create_comment)
comment_bp.route('/comments', methods=['GET'])(get_comments)
comment_bp.route('/comments/<int:comment_id>', methods=['GET'])(get_comment)
comment_bp.route('/comments/<int:comment_id>', methods=['PUT'])(update_comment)
comment_bp.route('/comments/<int:comment_id>', methods=['DELETE'])(delete_comment)
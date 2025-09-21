from flask import Blueprint
from controllers.gallery_controller import (
    create_gallery_image, get_gallery_images, get_gallery_image, update_gallery_image, delete_gallery_image
)

gallery_bp = Blueprint('gallery_bp', __name__)

gallery_bp.route('/gallery-images', methods=['POST'])(create_gallery_image)
gallery_bp.route('/gallery-images', methods=['GET'])(get_gallery_images)
gallery_bp.route('/gallery-images/<int:image_id>', methods=['GET'])(get_gallery_image)
gallery_bp.route('/gallery-images/<int:image_id>', methods=['PUT'])(update_gallery_image)
gallery_bp.route('/gallery-images/<int:image_id>', methods=['DELETE'])(delete_gallery_image)
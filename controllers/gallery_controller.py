from flask import request, jsonify
from models import db, GalleryImage
def gallery_to_dict(image):
    return {
        'id': image.id,
        'urls': image.urls.split('\n') if image.urls else [],
        'alt_text': image.alt_text,
        'description': image.description,
        'is_active': image.is_active,
        'created_at': image.created_at.isoformat() if image.created_at else None
    }

def create_gallery_image():
    data = request.get_json()
    urls = data.get('urls')
    if not urls:
        return jsonify({'error': 'urls es requerido'}), 400
    image = GalleryImage(
        urls='\n'.join(urls) if isinstance(urls, list) else urls,
        alt_text=data.get('alt_text'),
        description=data.get('description')
    )
    db.session.add(image)
    db.session.commit()
    return jsonify(gallery_to_dict(image)), 201

def get_gallery_images():
    images = GalleryImage.query.filter_by(is_active=True).all()
    return jsonify([gallery_to_dict(img) for img in images]), 200

def get_gallery_image(image_id):
    image = GalleryImage.query.get_or_404(image_id)
    if not image.is_active:
        return jsonify({'error': 'Imagen no encontrada'}), 404
    return jsonify(gallery_to_dict(image)), 200

def update_gallery_image(image_id):
    image = GalleryImage.query.get_or_404(image_id)
    data = request.get_json()
    urls = data.get('urls')
    if urls is not None:
        image.urls = '\n'.join(urls) if isinstance(urls, list) else urls
    image.alt_text = data.get('alt_text', image.alt_text)
    image.description = data.get('description', image.description)
    db.session.commit()
    return jsonify(gallery_to_dict(image)), 200

def delete_gallery_image(image_id):
    image = GalleryImage.query.get_or_404(image_id)
    image.is_active = False
    db.session.commit()
    return jsonify({'message': 'Imagen desactivada'}), 200
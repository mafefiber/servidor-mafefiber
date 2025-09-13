from flask import request, jsonify
from models import db, PlanFeature, Plan

def feature_to_dict(feature):
    return {
        'id': feature.id,
        'plan_id': feature.plan_id,
        'feature': feature.feature,
        'value': feature.value,
        'is_active': feature.is_active,
        'created_at': feature.created_at.isoformat() if feature.created_at else None
    }

def create_feature(plan_id):
    """
    Agregar característica a un plan
    ---
    tags:
      - PlanFeatures
    parameters:
      - in: path
        name: plan_id
        type: integer
        required: true
        description: ID del plan
      - in: body
        name: body
        schema:
          type: object
          required:
            - feature
          properties:
            feature:
              type: string
            value:
              type: string
    responses:
      201:
        description: Característica creada
        schema:
          type: object
          properties:
            id:
              type: integer
            feature:
              type: string
            value:
              type: string
      400:
        description: Faltan datos
    """
    Plan.query.get_or_404(plan_id)
    data = request.get_json() or {}
    feature = data.get('feature')
    value = data.get('value')
    if not feature:
        return jsonify({'error': 'Falta campo feature'}), 400
    pf = PlanFeature(plan_id=plan_id, feature=feature, value=value)
    db.session.add(pf)
    db.session.commit()
    return jsonify(feature_to_dict(pf)), 201

def get_features_by_plan(plan_id):
    """
    Listar características de un plan
    ---
    tags:
      - PlanFeatures
    parameters:
      - in: path
        name: plan_id
        type: integer
        required: true
        description: ID del plan
    responses:
      200:
        description: Lista de características
        schema:
          type: array
          items:
            type: object
    """
    Plan.query.get_or_404(plan_id)
    items = PlanFeature.query.filter_by(plan_id=plan_id, is_active=True).all()
    return jsonify([feature_to_dict(i) for i in items]), 200

def update_feature(feature_id):
    """
    Editar característica de un plan
    ---
    tags:
      - PlanFeatures
    parameters:
      - in: path
        name: feature_id
        type: integer
        required: true
        description: ID de la característica
      - in: body
        name: body
        schema:
          type: object
          properties:
            feature:
              type: string
            value:
              type: string
            is_active:
              type: boolean
    responses:
      200:
        description: Característica actualizada
      404:
        description: No existe la característica
    """
    pf = PlanFeature.query.get_or_404(feature_id)
    data = request.get_json() or {}
    pf.feature = data.get('feature', pf.feature)
    pf.value = data.get('value', pf.value)
    if 'is_active' in data:
        pf.is_active = bool(data.get('is_active'))
    db.session.commit()
    return jsonify(feature_to_dict(pf)), 200

def delete_feature(feature_id):
    """
    Eliminar/desactivar característica (soft delete)
    ---
    tags:
      - PlanFeatures
    parameters:
      - in: path
        name: feature_id
        type: integer
        required: true
        description: ID de la característica
    responses:
      200:
        description: Característica desactivada
      404:
        description: No existe la característica
    """
    pf = PlanFeature.query.get_or_404(feature_id)
    pf.is_active = False
    db.session.commit()
    return jsonify({'message': 'Característica desactivada'}), 200
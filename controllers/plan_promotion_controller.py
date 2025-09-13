from flask import request, jsonify
from models import db, PlanPromotion, Plan, Promotions

def pp_to_dict(pp):
    return {
        'id': pp.id,
        'plan_id': pp.plan_id,
        'promotion_id': pp.promotion_id,
        'is_active': pp.is_active,
        'created_at': pp.created_at.isoformat() if pp.created_at else None
    }

def associate_promotion(plan_id):
    """
    Asociar promoción a un plan
    ---
    tags:
      - PlanPromotions
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
            - promotion_id
          properties:
            promotion_id:
              type: integer
    responses:
      201:
        description: Promoción asociada al plan
      400:
        description: Datos inválidos
      404:
        description: Plan o promoción no encontrados
    """
    Plan.query.get_or_404(plan_id)
    data = request.get_json() or {}
    promotion_id = data.get('promotion_id')
    if not promotion_id:
        return jsonify({'error': 'Falta promotion_id'}), 400
    Promotions.query.get_or_404(promotion_id)
    pp = PlanPromotion(plan_id=plan_id, promotion_id=promotion_id)
    db.session.add(pp)
    db.session.commit()
    return jsonify(pp_to_dict(pp)), 201

def list_promotions_by_plan(plan_id):
    """
    Listar promociones asociadas a un plan
    ---
    tags:
      - PlanPromotions
    parameters:
      - in: path
        name: plan_id
        type: integer
        required: true
        description: ID del plan
    responses:
      200:
        description: Lista de promociones asociadas
        schema:
          type: array
          items:
            $ref: '#/definitions/PlanPromotion'
      404:
        description: Plan no encontrado
    """
    Plan.query.get_or_404(plan_id)
    items = PlanPromotion.query.filter_by(plan_id=plan_id, is_active=True).all()
    return jsonify([pp_to_dict(i) for i in items]), 200

def remove_plan_promotion(pp_id):
    """
    Desactivar asociación promoción-plan (soft delete)
    ---
    tags:
      - PlanPromotions
    parameters:
      - in: path
        name: pp_id
        type: integer
        required: true
        description: ID de la asociación a desactivar
    responses:
      200:
        description: Asociación desactivada
      404:
        description: Asociación no encontrada
    """
    pp = PlanPromotion.query.get_or_404(pp_id)
    pp.is_active = False
    db.session.commit()
    return jsonify({'message': 'Asociación desactivada'}), 200
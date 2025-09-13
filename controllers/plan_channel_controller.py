from flask import request, jsonify
from models import db, PlanFeature, Plan,Channel

def pc_to_dict(pc):
    return{
        'id':pc.id,
        'plan_id':pc.plan_id,
        'channel_id':pc.channel_id,
        'is_active':pc.is_active,
        'created_at':pc.created_at.isoformat() if pc.created_at else None
    }
def associate_channel(plan_id):
    """
    Asociar canal a un plan
    ---
    tags:
      - PlanChannels
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
            - channel_id
          properties:
            channel_id:
              type: integer
    responses:
      201:
        description: Canal asociado al plan
      400:
        description: Datos inválidos
      404:
        description: Plan o canal no encontrados
    """
    Plan.query.get_or_404(plan_id)
    data = request.get_json() or {}
    channel_id = data.get('channel_id')
    if not channel_id:
        return jsonify({'error': 'Falta channel_id'}), 400
    Channel.query.get_or_404(channel_id)
    pc = PlanFeature(plan_id=plan_id, channel_id=channel_id)
    db.session.add(pc)
    db.session.commit()
    return jsonify(pc_to_dict(pc)), 201

def list_channels_by_plan(plan_id):
    """
    Listar canales asociados a un plan
    ---
    tags:
      - PlanChannels
    parameters:
      - in: path
        name: plan_id
        type: integer
        required: true
        description: ID del plan
    responses:
      200:
        description: Lista de canales del plan
        schema:
          type: array
          items:
            $ref: '#/definitions/PlanChannel'
      404:
        description: Plan no encontrado
    """
    plan.query.get_or_404(plan_id)
    pcs = PlanChannel.query.filter_by(plan_id=plan_id, is_active=True).all()
    return jsonify([pc_to_dict(i) for i in items]), 200

def remove_plan_channel(pc_id):
    """
    Desactivar asociación canal-plan (soft delete)
    ---
    tags:
      - PlanChannels
    parameters:
      - in: path
        name: pc_id
        type: integer
        required: true
        description: ID de la asociación a desactivar
    responses:
      200:
        description: Asociación desactivada
      404:
        description: Asociación no encontrada
    """
    pc = PlanChannel.query.get_or_404(pc_id)
    pc.is_active = False
    db.session.commit()
    return jsonify({'message': 'Asociación desactivada'}), 200
    
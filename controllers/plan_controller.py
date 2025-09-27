from flask import request,jsonify
from models import db,Plan

def plan_to_dict(plan):
    return{
        'id':plan.id,
        'name':plan.name,
        'speed_mbps':plan.speed_mbps,
        'price':float(plan.price),
        'technology':plan.technology,
        'description':plan.description,
        'features': plan.features,  # <-- Agregado aquí
        'is_active':plan.is_active,
        'created_at':plan.created_at.isoformat() if plan.created_at else None
    }
def create_plan():
    """
    Crear un nuevo plan de internet
    ---
    tags:
      - Planes
    parameters:
      - in: body
        name: plan
        required: true
        description: Datos del nuevo plan
        schema:
          type: object
          required:
            - name
            - speed_mbps
            - price
            - technology
          properties:
            name:
              type: string
              description: Nombre del plan
            speed_mbps:
              type: integer
              description: Velocidad en Mbps
            price:
              type: number
              description: Precio del plan
            technology:
              type: string
              description: Tecnología utilizada
            description:
              type: string
              description: Descripción del plan
    responses:
      201:
        description: Plan creado exitosamente
        schema:
          $ref: '#/definitions/Plan'
      400:
        description: Faltan datos requeridos
    """
    data=request.get_json()
    name = data.get('name')
    speed_mbps = data.get('speed_mbps')
    price = data.get('price')
    technology = data.get('technology')
    description = data.get('description')
    features = data.get('features')  # <-- Agregado aquí

    if not name or not speed_mbps or not price or not technology:
        return jsonify({'error':'Faltan datos requeridos'}),400

    plan=Plan(
    name=name,
    speed_mbps=speed_mbps,
    price=price,
    technology=technology,
    description=description,
    features=features  # <-- Agregado aquí
  )
    db.session.add(plan)
    db.session.commit()   
    return jsonify(plan_to_dict(plan)),201

def get_plans():
    """
    Obtener lista de todos los planes activos
    ---
    tags:
      - Planes
    responses:
      200:
        description: Lista de planes obtenida exitosamente
        schema:
          type: array
          items:
            $ref: '#/definitions/Plan'
    """
    plans = Plan.query.filter_by(is_active=True).all()
    return jsonify([plan_to_dict(p) for p in plans]),200

def get_plan(plan_id):
    """
    Obtener un plan específico por ID
    ---
    tags:
      - Planes
    parameters:
      - in: path
        name: plan_id
        type: integer
        required: true
        description: ID del plan a consultar
    responses:
      200:
        description: Plan encontrado exitosamente
        schema:
          $ref: '#/definitions/Plan'
      404:
        description: Plan no encontrado
    """
    plan = Plan.query.get_or_404(plan_id)
    if not plan.is_active:
        return jsonify({'error':'Plan no encontrado'}),404
    return jsonify(plan_to_dict(plan)),200

def update_plan(plan_id):
    """
    Actualizar un plan existente
    ---
    tags:
      - Planes
    parameters:
      - in: path
        name: plan_id
        type: integer
        required: true
        description: ID del plan a actualizar
      - in: body
        name: plan
        required: true
        description: Nuevos datos del plan
        schema:
          type: object
          properties:
            name:
              type: string
            speed_mbps:
              type: integer
            price:
              type: number
            technology:
              type: string
            description:
              type: string
    responses:
      200:
        description: Plan actualizado exitosamente
        schema:
          $ref: '#/definitions/Plan'
      404:
        description: Plan no encontrado
    """
    plan=Plan.query.get_or_404(plan_id)
    data=request.get_json()
    plan.name=data.get('name',plan.name)
    plan.speed_mbps=data.get('speed_mbps',plan.speed_mbps)
    plan.price=data.get('price',plan.price)
    plan.technology=data.get('technology',plan.technology)
    plan.description=data.get('description',plan.description)
    plan.features = data.get('features', plan.features)  # <-- Agregado aquí
    db.session.commit()
    return jsonify(plan_to_dict(plan)),200

def delete_plan(plan_id):
    """
    Desactivar un plan (soft delete)
    ---
    tags:
      - Planes
    parameters:
      - in: path
        name: plan_id
        type: integer
        required: true
        description: ID del plan a desactivar
    responses:
      200:
        description: Plan desactivado exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Plan no encontrado
    """
    plan=Plan.query.get_or_404(plan_id)
    plan.is_active=False
    db.session.commit()
    return jsonify({'message':'Plan desactivado'}),200

# (La documentación ahora está en los docstrings de cada función para que Flasgger la detecte)

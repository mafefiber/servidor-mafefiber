from flask import Blueprint, request
from controllers.auth_controller import(
     register_user,login_user,logout_token,me_user,refresh_token,
    request_password_reset, reset_password_width_token, change_password
)
from auth import auth_required,_extract_bearer
from flask import g

auth_bp = Blueprint('auth',__name__)

@auth_bp.post('/auth/register')
def register():
    data = request.get_json(force=True,silent=True) or {}
    return register_user(
        username=data.get("username",""),
        email=data.get("email",""),
        password=data.get("password",""),
        full_name=data.get("full_name",""),
    )

@auth_bp.post('/auth/login')
def login():
    data = request.get_json(force=True,silent=True) or {}
    return login_user(
        username_or_email=data.get("usernameOrEmail",""),
        password=data.get("password",""),
        hours=int(data.get("hours",24)),
    )

@auth_bp.post('/auth/logout')
@auth_required
def logout():
    token = _extract_bearer()
    return logout_token(token)

@auth_bp.get('/auth/me')
@auth_required
def me():
    return me_user(g.current_user)

@auth_bp.post('/auth/refresh')
@auth_required
def refresh():
    old_token = _extract_bearer()
    return refresh_token(old_token,hours=24)

@auth_bp.route('/forgot-password',methods=['POST'])
def forgot_password():
    data = request.get_json()
    if not data or 'email' not in data:
        return {"error": "El campo 'email' es obligatorio."}, 400

    return request_password_reset(data['email'])

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    if not data or 'token' not in data or 'new_password' not in data:
        return {"error": "Los campos 'token' y 'new_password' son obligatorios."}, 400
    return reset_password_width_token(data['token'], data['new_password'])
@auth_bp.route('/change-password', methods=['POST'])
@auth_required  # ¡Importante! Requiere autenticación
def change_password():
    data = request.get_json()
    if not data or 'old_password' not in data or 'new_password' not in data:
        return {"error": "Los campos 'old_password' y 'new_password' son obligatorios."}, 400
    return change_password(g.current_user, data['old_password'], data['new_password'])

@auth_bp.get('/auth/users')
@auth_required
def get_users():
    if not getattr(g.current_user, "id_admin", False):
        return {"error": "Solo administradores"}, 403
    from controllers.auth_controller import get_all_users
    return get_all_users()

@auth_bp.get('/auth/users/<int:user_id>')
@auth_required
def get_user(user_id):
    if not getattr(g.current_user, "id_admin", False):
        return {"error": "Solo administradores"}, 403
    from controllers.auth_controller import get_user_by_id
    return get_user_by_id(user_id)

@auth_bp.put('/auth/users/<int:user_id>')
@auth_required
def update_user(user_id):
    if not getattr(g.current_user, "id_admin", False):
        return {"error": "Solo administradores"}, 403
    data = request.get_json() or {}
    from controllers.auth_controller import update_user_by_id
    return update_user_by_id(user_id, data)

@auth_bp.patch('/auth/users/<int:user_id>/deactivate')
@auth_required
def deactivate_user(user_id):
    if not getattr(g.current_user, "id_admin", False):
        return {"error": "Solo administradores"}, 403
    from controllers.auth_controller import deactivate_user_by_id
    return deactivate_user_by_id(user_id)


@auth_bp.patch('/auth/users/<int:user_id>/activate')
@auth_required
def activate_user(user_id):
    if not getattr(g.current_user, "id_admin", False):
        return {"error": "Solo administradores"}, 403
    from controllers.auth_controller import activate_user_by_id
    return activate_user_by_id(user_id)

@auth_bp.get('/auth/users/search')
@auth_required
def search_users_route():
    if not getattr(g.current_user,"id_admin",False):
        return {"error":"Solo administradores"},403
    query = request.args.get('q','')
    from controllers.auth_controller import search_users
    return search_users(query)
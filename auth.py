from functools import wraps
from flask import request, jsonify,g
from datetime import timezone
from models import User,db,UserToken
from security import now_utc

def _extract_bearer():
    auth =request.headers.get("Authorization", "")
    if not auth.startswith("Bearer"):
        return None
    return auth.split(" ",1)[1].strip() or None

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = _extract_bearer()
        if not token:
            return jsonify({"msg":"Token no proporcionado"}),401
        ut = UserToken.query.filter_by(token=token,is_active=True).first()
        if not ut or (ut.expires_at and ut.expires_at.replace(tzinfo=timezone.utc)< now_utc()):
            return jsonify({"msg":"Token inválido o expirado"}),401
        user = User.query.get(ut.user_id)
        if not user or not user.is_active:
            return jsonify({"msg":"Usuario no encontrado o inactivo"}),403
        g.current_user = user
        g.current_token = ut
        return fn(*args, **kwargs)
    return wrapper
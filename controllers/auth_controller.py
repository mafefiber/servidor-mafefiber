from datetime import datetime, timedelta
import os
from models import db, User, PasswordResetToken
from security import hash_password,check_password,generate_token,expiry,now_utc
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import jsonify
import requests

def register_user(username,email,password,full_name=None):
    if User.query.filter(or_(User.username==username,User.email==email)).first():
        return jsonify({"error":"El nombre de usuario o correo ya existe"}),400
    user = User(
        username=username.strip(),
        email=email.strip().lower(),
        password_hash=hash_password(password),
        full_name=full_name or "",
        id_admin=False,
        is_active=True,
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"ok":True,"user":_public_user(user)}),201

def login_user(username_or_email,password,hours=24):
    user =User.query.filter(
        or_(User.username==username_or_email, User.email==username_or_email.lower())
    ).first()
    if not user or not check_password(password,user.password_hash):
        return jsonify({"error":"Credenciales inválidas"}),401
    tok=UserToken(
        user_id=user.id,
        token=generate_token(),
        expiries_at=expiry(hours),
        is_active=True,
    )
    db.session.add(tok)
    db.session.commit()
    return jsonify({
        "token":tok.token,
        "expires_at":tok.expiries_at.isoformat(),
        "user":_public_user(user),

    }),200

def logout_token(token:str):
    ut = userToken.query.filter_by(token=token,is_active=True).first()
    if not ut:
        return jsonify({"ok":True})
    ut.is_active=False
    db.session.commit()
    return jsonify({"ok":True})

def me_user(user:User):
    return jsonify({"user":_public_user(user)}),200

def refresh_token(old_token:str,hours=24):
    ut = UserToken.query.filter_by(token=old_token,is_active=True).first()
    if not ut:
        return jsonify({"error":"Token inválido"}),401
    
    #optional invalidation of old token
    ut.is_active=False
    new_tok=UserToken(
        user_id=ut.user_id,
        token=generate_token(),
        expires_at=expiry(hours),
        is_active=True,
    )

    db.session.add(new_tok)
    db.session.commit()
    return jsonify({
        "token":new_tok.token,
        "expires_at":new_tok.expires_at.isoformat(),
    }),200

def _public_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "id_admin": user.id_admin,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }

#reset password
def request_password_reset(email):
    """Recibir un correo para restablecer la contraseña"""
    user = User.query.filter_by(email=email.lower()).first()
    if not user:
        return jsonify({'error':'Correo no encontrado'}), 404
    
    #generar token unique
    token = generate_token()
    expiry=datetime.utcnow() + timedelta(hours=24)

    #create reset token
    reset_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=expiry,
    )
    db.session.add(reset_token)
    db.session.commit()

    # send email
    try:
        send_reset_email(user.email,token)
        return jsonify({"ok":True,"msg":"Correo de restablecimiento enviado"}),200
    except Exception as e:
        print("Error al enviar el correo de recuperación:", repr(e))  # <-- LOG DEL ERROR
        db.session.delete(reset_token)
        db.session.commit()
        return jsonify({"error":"Error al enviar el correo"}),500

def reset_password_width_token(token,new_password):
    """Restablecer la contraseña usando el token"""
    reset_token = PasswordResetToken.query.filter_by(
        token=token,
        is_used=False
    ).first()

    if not reset_token:
        return jsonify({"error":"Token inválido o ya usado"}),400
    
    #token expiry check
    if reset_token.expires_at.replace(tzinfo=None) < now_utc().replace(tzinfo=None):
    return jsonify({"error":"Token expirado"}),400
    #update user password
    user = User.query.get(reset_token.user_id)
    user.password_hash = hash_password(new_password)

    #mark token as used
    reset_token.is_used = True

    db.session.commit()
    return jsonify({"ok":True,"msg":"Contraseña restablecida"}),200

def send_reset_email(email, token):
    """Enviar correo de restablecimiento de contraseña usando Brevo API"""
    brevo_api_key = os.getenv('BREVO_API_KEY')
    reset_url = f"{os.getenv('FRONTEND_URL','https://mafefiber-production.up.railway.app')}/reset-password?token={token}"

    body = f"""
    <p>Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace para continuar:</p>
    <p><a href="{reset_url}">Restablecer contraseña</a></p>
    <p>Si no solicitaste este cambio, puedes ignorar este correo.</p>
    <p>El enlace expirará en 24 horas.</p>
    """

    data = {
        "sender": {"name": "Mafefiber", "email": "cjair759@gmail.com"},  # Usa tu correo verificado en Brevo
        "to": [{"email": email}],
        "subject": "Restablecimiento de contraseña - Mafefiber",
        "htmlContent": body
    }

    headers = {
        "accept": "application/json",
        "api-key": brevo_api_key,
        "content-type": "application/json"
    }

    response = requests.post("https://api.brevo.com/v3/smtp/email", json=data, headers=headers)
    print("Brevo response:", response.status_code, response.text)
    response.raise_for_status()  # Lanza excepción si hay error

#change password
def change_password(user,old_password,new_password):
    """Cambiar la contraseña del usuario autenticado"""
    if not check_password(old_password,user.password_hash):
        return jsonify({"error":"Contraseña actual incorrecta"}),400
    
    user.password_hash = hash_password(new_password)
    db.session.commit()
    return jsonify({"ok":True,"msg":"Contraseña cambiada"}),200


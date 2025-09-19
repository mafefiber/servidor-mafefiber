import secrets
from datetime import datetime,timedelta,timezone
import bcrypt

TOKEN_BYTES = 32

def hash_password(password:str) ->str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password:str, password_hash:str) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception:
        return False   

def generate_token()->str:
    return secrets.token_urlsafe(TOKEN_BYTES)

def expiry(hours:int=24)->datetime:
    return datetime.now(timezone.utc) + timedelta(hours=hours)

def now_utc()->datetime:
    return datetime.now(timezone.utc)
import jwt
import datetime
from fastapi import HTTPException, Request
from ..config import Config

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload.get("user_id")
    except jwt.InvalidTokenError:
        return None

async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = auth_header.split(" ")[1]
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_id
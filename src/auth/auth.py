import datetime

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlmodel import select
from starlette import status

from db import get_session
from models.user_models import User


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"])
    secret = "supersecret"

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, pwd, hash_pwd):
        return self.pwd_context.verify(pwd, hash_pwd)

    def encode_token(self, user_id):
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired signature")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
        )
        username = self.decode_token(auth.credentials)
        if username is None:
            raise credentials_exception
        user = get_session().exec(select(User).where(User.username == username)).first()
        if user is None:
            raise credentials_exception
        return user

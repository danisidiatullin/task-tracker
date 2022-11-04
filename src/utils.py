from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from auth.auth import AuthHandler
from db import get_session
from models import User
from models.user import Role

auth_handler = AuthHandler()


class RoleChecker:
    def __init__(self, roles: list[Role]):
        self.roles = roles

    def __call__(self, user=Depends(auth_handler.auth_wrapper), session: Session = Depends(get_session)):
        user_found = session.exec(select(User).where(User.username == user)).first()
        if user_found.role not in self.roles:
            raise HTTPException(status_code=403, detail="You are not a manager!")

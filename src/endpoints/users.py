import os

import boto3
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlmodel import Session, select

from auth.auth import AuthHandler
from config import settings
from db import get_session
from models.user import ChangePassword, Role, User, UserCreate, UserLogin, UserRead, UserRoleUpdate
from utils import RoleChecker

router = APIRouter(tags=["users"])
auth_handler = AuthHandler()


@router.post("/signup/", status_code=status.HTTP_201_CREATED, description="Register new user")
def signup(*, session: Session = Depends(get_session), user: UserCreate):
    users = session.exec(select(User)).all()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail="Username is taken")
    hashed_pwd = auth_handler.get_password_hash(user.password)
    user = User(username=user.username, password=hashed_pwd, email=user.email, role=user.role)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/login/")
def login(*, session: Session = Depends(get_session), user: UserLogin):
    user_found = session.exec(select(User).where(User.username == user.username)).first()
    if not user_found:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username and/or password")
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username and/or password")
    token = auth_handler.encode_token(user_found.username)
    return {"token": token}


@router.post("/change_password/")
def change_password(
    *, session: Session = Depends(get_session), user=Depends(auth_handler.auth_wrapper), passwords: ChangePassword
):
    user_found = session.exec(select(User).where(User.username == user)).first()
    verified = auth_handler.verify_password(passwords.old_password, user_found.password)
    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid old password")

    hashed_new_pwd = auth_handler.get_password_hash(passwords.new_password)
    user_found.password = hashed_new_pwd
    session.add(user_found)
    session.commit()
    session.refresh(user_found)

    return {"detail": "Password updated"}


@router.get("/users/me/", response_model=UserRead)
def get_current_user(*, session: Session = Depends(get_session), user=Depends(auth_handler.auth_wrapper)):
    user_found = session.exec(select(User).where(User.username == user)).first()
    return user_found


@router.post("/upload_photo/", response_model=UserRead)
def upload_photo(
    *, session: Session = Depends(get_session), user=Depends(auth_handler.auth_wrapper), data: UploadFile = File(...)
):
    user_found = session.exec(select(User).where(User.username == user)).first()
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.access_key,
        aws_secret_access_key=settings.secret_key,
    )

    key = os.urandom(8).hex() + ".jpg"
    s3.put_object(
        Bucket=settings.bucket,
        Key=key,
        Body=data.file,
        ContentType="image/jpg",
    )

    user_found.photo = key
    session.add(user_found)
    session.commit()
    session.refresh(user_found)

    return user_found


@router.patch("/users/{user_id}/", response_model=UserRead, dependencies=[Depends(RoleChecker(Role.manager))])
def update_user_role(*, session: Session = Depends(get_session), user_id: int, user: UserRoleUpdate):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.role = user.role
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

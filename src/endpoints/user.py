from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette import status

from auth.auth import AuthHandler
from db import get_session
from models.user_models import User, UserLogin, UserCreate, UserRead

router = APIRouter()
auth_handler = AuthHandler()


@router.post('/signup/', status_code=status.HTTP_201_CREATED, tags=['users'], description='Register new user')
def signup(*, session: Session = Depends(get_session), user: UserCreate):
    users = session.exec(select(User)).all()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    user = User(username=user.username,
                password=hashed_pwd,
                email=user.email,
                role=user.role)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post('/login/', tags=['users'])
def login(*, session: Session = Depends(get_session), user: UserLogin):
    user_found = session.exec(select(User).where(User.username == user.username)).first()
    if not user_found:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user_found.username)
    return {'token': token}


@router.get('/users/me/', tags=['users'], response_model=UserRead)
def get_current_user(*, session: Session = Depends(get_session), user=Depends(auth_handler.auth_wrapper)):
    user_found = session.exec(select(User).where(User.username == user)).first()
    return user_found


from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from models import User, get_session

router = APIRouter()


@router.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
def get_users(
    *,
    session: Session = Depends(get_session),
):
    users = session.exec(select(User)).all()

    return users


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(*, session: Session = Depends(get_session), user: User):
    new_user = User.from_orm(user)

    session.add(new_user)

    session.commit()
    session.refresh(new_user)

    return new_user

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from starlette import status

from db import get_session
from endpoints.users import auth_handler
from models import User
from models.task import Task, TaskCreate, TaskRead, TaskReadWithBoard, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(*, session: Session = Depends(get_session), task: TaskCreate, user=Depends(auth_handler.auth_wrapper)):
    user_found = session.exec(select(User).where(User.username == user)).first()
    task.user_id = user_found.id
    db_task = Task.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/", response_model=List[TaskRead])
def read_tasks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=1000),
):
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
    return tasks


@router.get("/{task_id}/", response_model=TaskReadWithBoard)
def read_task(*, session: Session = Depends(get_session), task_id: int):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(*, session: Session = Depends(get_session), task_id: int):

    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}


@router.patch("/{task_id}/", response_model=TaskRead)
def partial_update_task(*, session: Session = Depends(get_session), task_id: int, task: TaskUpdate):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

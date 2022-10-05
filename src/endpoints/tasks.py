from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from models import Task, get_session

router = APIRouter()


@router.get("/tasks", response_model=List[Task], status_code=status.HTTP_200_OK)
def get_tasks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()

    return tasks


@router.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks", response_model=Task)
def create_task(*, session: Session = Depends(get_session), task: Task):
    new_task = Task.from_orm(task)

    session.add(new_task)

    session.commit()
    session.refresh(new_task)

    return new_task

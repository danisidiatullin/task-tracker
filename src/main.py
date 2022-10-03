from typing import List

from fastapi import Depends, FastAPI, Query, status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, SQLModel, create_engine, select

from models import Task, User

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/postgres_db", echo=True
)

SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
def get_users(
    *,
    session: Session = Depends(get_session),
):
    users = session.exec(select(User)).all()

    return users


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(*, session: Session = Depends(get_session), user: User):
    new_user = User.from_orm(user)

    session.add(new_user)

    session.commit()
    session.refresh(new_user)

    return new_user


@app.get("/tasks", response_model=List[Task], status_code=status.HTTP_200_OK)
def get_tasks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()

    return tasks


@app.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(*, session: Session = Depends(get_session), task: Task):
    new_task = Task.from_orm(task)

    session.add(new_task)

    session.commit()
    session.refresh(new_task)

    return new_task

from typing import List, Optional, Union

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, select
from starlette import status

from db import engine
from models.board_models import Board, BoardCreate, BoardRead, BoardUpdate
from models.task_models import Task, TaskCreate, TaskRead, TaskUpdate


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = False


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/tasks/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(*, session: Session = Depends(get_session), task: TaskCreate):
    db_task = Task.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.get("/tasks/", response_model=List[TaskRead])
def read_tasks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=1000),
):
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
    return tasks


@app.get("/tasks/{task_id}/", response_model=TaskRead)
def read_task(*, session: Session = Depends(get_session), task_id: int):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(*, session: Session = Depends(get_session), task_id: int):

    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}


@app.patch("/tasks/{task_id}/", response_model=TaskRead)
def partial_update_task(
    *, session: Session = Depends(get_session), task_id: int, task: TaskUpdate
):
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


@app.post("/boards/", response_model=BoardRead)
def create_board(*, session: Session = Depends(get_session), team: BoardCreate):
    db_team = Board.from_orm(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.get("/boards/", response_model=List[BoardRead])
def read_boards(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    boards = session.exec(select(Board).offset(offset).limit(limit)).all()
    return boards


@app.get("/boards/{board_id}", response_model=BoardRead)
def read_board(*, board_id: int, session: Session = Depends(get_session)):
    board = session.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


@app.patch("/boards/{board_id}", response_model=BoardRead)
def update_board(
    *,
    session: Session = Depends(get_session),
    board_id: int,
    board: BoardUpdate,
):
    db_board = session.get(Board, board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    board_data = board.dict(exclude_unset=True)
    for key, value in board_data.items():
        setattr(db_board, key, value)
    session.add(db_board)
    session.commit()
    session.refresh(db_board)
    return db_board


@app.delete("/boards/{board_id}")
def delete_board(*, session: Session = Depends(get_session), board_id: int):
    board = session.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(board)
    session.commit()
    return {"ok": True}


# app.include_router(root.router)
# app.include_router(pathparams.router)
# app.include_router(queryparams.router)
# app.include_router(bodyparams.router)

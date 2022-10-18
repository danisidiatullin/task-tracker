import enum
from typing import Optional

from sqlmodel import Column, Enum, Field, Relationship, SQLModel


class Status(enum.Enum):
    started = "started"
    finished = "finished"


class TaskBase(SQLModel):
    title: str
    description: str
    status: Status
    priority: int = 10
    progress: int = 0

    board_id: Optional[int] = Field(default=None, foreign_key="board.id")


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    board: Optional["Board"] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    priority: Optional[int] = None
    progress: Optional[int] = None
    board_id: Optional[int] = None

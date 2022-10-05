import enum
from typing import Optional, Union

from sqlmodel import Column, Enum, Field, Session, SQLModel, create_engine


class Status(str, enum.Enum):
    started = "started"
    finished = "finished"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    status: Status = Field(sa_column=Column(Enum(Status)))
    priority: int
    progress: int
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


engine = create_engine(
    "postgresql://postgres:postgres@postgres/postgres_db",  # for running in docker
    # "postgresql://postgres:postgres@localhost:5432/postgres_db",   # for pytest
    echo=True,
)

SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
